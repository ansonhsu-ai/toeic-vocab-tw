/**
 * 模組名稱：test_srs_logic.js
 * 測試說明：測試 JavaScript 版 CSV 解析防呆、SRS 佇列操作演算法與例句語音萃取邏輯
 */

const assert = require('assert');

// 1. CSV 解析器測試實作
class CsvParserService {
    static parse(csvText) {
        if (!csvText || typeof csvText !== 'string' || !csvText.trim()) {
            throw new Error('CSV 檔案為空或內容無效');
        }

        const rows = [];
        let currentRow = [];
        let currentField = '';
        let insideQuotes = false;
        let i = 0;

        // 去除可能的 BOM
        let text = csvText.charCodeAt(0) === 0xFEFF ? csvText.slice(1) : csvText;

        while (i < text.length) {
            const char = text[i];
            const nextChar = text[i + 1];

            if (char === '"') {
                if (insideQuotes && nextChar === '"') {
                    currentField += '"';
                    i += 2;
                    continue;
                } else {
                    insideQuotes = !insideQuotes;
                    i++;
                    continue;
                }
            }

            if (!insideQuotes && char === ',') {
                currentRow.push(currentField.trim());
                currentField = '';
                i++;
                continue;
            }

            if (!insideQuotes && (char === '\r' || char === '\n')) {
                if (char === '\r' && nextChar === '\n') {
                    i++;
                }
                currentRow.push(currentField.trim());
                currentField = '';
                if (currentRow.some(f => f.length > 0)) {
                    rows.push(currentRow);
                }
                currentRow = [];
                i++;
                continue;
            }

            currentField += char;
            i++;
        }

        if (currentField.length > 0 || currentRow.length > 0) {
            currentRow.push(currentField.trim());
            if (currentRow.some(f => f.length > 0)) {
                rows.push(currentRow);
            }
        }

        if (rows.length === 0) {
            throw new Error('CSV 檔案中未發現有效資料列');
        }

        // 轉換為 Flashcard 清單
        const cards = [];
        for (let rIndex = 0; rIndex < rows.length; rIndex++) {
            const row = rows[rIndex];
            const word = row[0] || '';
            const content = row.slice(1).join('\n') || '';

            if (word) {
                cards.push({
                    id: rIndex + 1,
                    word: word.trim(),
                    content: content.trim()
                });
            }
        }

        if (cards.length === 0) {
            throw new Error('未能自 CSV 中成功解析出任何單字卡片');
        }

        return cards;
    }
}

// 2. SRS 佇列引擎測試實作
class SrsEngine {
    constructor(cards = []) {
        this.cards = [...cards];
        this.queue = [...cards];
        this.stats = { again: 0, hard: 0, known: 0, easy: 0 };
    }

    getCurrentCard() {
        return this.queue.length > 0 ? this.queue[0] : null;
    }

    isFinished() {
        return this.queue.length === 0;
    }

    processAnswer(action) {
        if (this.queue.length === 0) return;
        const current = this.queue.shift();

        switch (action) {
            case 'again':
                this.stats.again++;
                // 插入佇列第 2 個位置 (index 1)
                if (this.queue.length >= 1) {
                    this.queue.splice(1, 0, current);
                } else {
                    this.queue.push(current);
                }
                break;

            case 'hard':
                this.stats.hard++;
                // 插入佇列剩餘長度的中間位置
                const mid = Math.floor(this.queue.length / 2);
                this.queue.splice(mid, 0, current);
                break;

            case 'known':
                this.stats.known++;
                // 插入佇列最尾端
                this.queue.push(current);
                break;

            case 'easy':
                this.stats.easy++;
                // 直接移出佇列
                break;

            default:
                throw new Error(`未知的 SRS 操作: ${action}`);
        }
    }
}

// 3. 例句英文提取測試
function extractEnglishExample(content) {
    if (!content) return '';
    const match = content.match(/【例句】\s*\n?([^\n(（]+)/);
    if (match && match[1]) {
        return match[1].trim();
    }
    return '';
}

// === 執行單元測試 ===
console.log('--- 測試 1: CSV 解析與雙引號換行 ---');
const sampleCsv = `ability,"ability (n.) 能力、才幹
【搭配詞】
academic ability 學術能力
【例句】
She has the ability. (她有能力。)"
accident,"accident (n.) 意外
【例句】
He had an accident. (他發生了意外。)"`;

const parsedCards = CsvParserService.parse(sampleCsv);
assert.strictEqual(parsedCards.length, 2);
assert.strictEqual(parsedCards[0].word, 'ability');
assert.strictEqual(parsedCards[1].word, 'accident');
assert.ok(parsedCards[0].content.includes('academic ability'));
console.log('✓ CSV 解析測試通過');

console.log('--- 測試 2: CSV 空白防呆 ---');
assert.throws(() => CsvParserService.parse('   '), /CSV 檔案為空/);
console.log('✓ 空白 CSV 防呆測試通過');

console.log('--- 測試 3: SRS 佇列操作規則 ---');
const engine = new SrsEngine([
    { id: 1, word: 'card1' },
    { id: 2, word: 'card2' },
    { id: 3, word: 'card3' },
    { id: 4, word: 'card4' }
]);

// 測試 Again (插入第 2 個位置: 目前 queue=[2,3,4], 插入 index 1 -> [2, 1, 3, 4])
engine.processAnswer('again');
assert.strictEqual(engine.queue[0].word, 'card2');
assert.strictEqual(engine.queue[1].word, 'card1');
assert.strictEqual(engine.stats.again, 1);
console.log('✓ Again 插入第 2 位置測試通過');

// 測試 Hard (當前 card2, queue 剩下 [1, 3, 4], length 3, mid=1 -> 插入 index 1 -> [1, 2, 3, 4])
engine.processAnswer('hard');
assert.strictEqual(engine.queue[0].word, 'card1');
assert.strictEqual(engine.queue[1].word, 'card2');
assert.strictEqual(engine.stats.hard, 1);
console.log('✓ Hard 插入中間位置測試通過');

// 測試 Known (當前 card1, queue 剩下 [2, 3, 4] -> push 尾端 -> [2, 3, 4, 1])
engine.processAnswer('known');
assert.strictEqual(engine.queue[3].word, 'card1');
assert.strictEqual(engine.stats.known, 1);
console.log('✓ Known 插入尾端測試通過');

// 測試 Easy (當前 card2, queue 剩下 [3, 4, 1] -> 直接移除)
engine.processAnswer('easy');
assert.strictEqual(engine.queue.length, 3);
assert.strictEqual(engine.stats.easy, 1);
console.log('✓ Easy 移除測試通過');

console.log('--- 測試 4: 例句英文提取 ---');
const contentSample = `ability (n.) 能力
【例句】
She has the ability to solve complex problems. (她有快速解決問題的能力。)`;
const extractedEn = extractEnglishExample(contentSample);
assert.strictEqual(extractedEn, 'She has the ability to solve complex problems.');
console.log('✓ 例句英文提取測試通過');

console.log('\n=== 所有 JavaScript 邏輯單元測試全數通過！ ===');
