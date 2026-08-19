/**
 * 模組名稱：test_session_checkin.js
 * 測試說明：驗證多字母分散隨機抽取、每日 Session 10 字管理與連續打卡 Streak 演算法
 */

const assert = require('assert');

// 模擬跨 A~Z 字母的多樣化單字庫
const mockAlphabetVocabulary = [
    { id: 1, word: 'apple', content: '蘋果' },
    { id: 2, word: 'apply', content: '申請' },
    { id: 3, word: 'banana', content: '香蕉' },
    { id: 4, word: 'business', content: '商業' },
    { id: 5, word: 'career', content: '職業' },
    { id: 6, word: 'customer', content: '顧客' },
    { id: 7, word: 'decision', content: '決定' },
    { id: 8, word: 'economy', content: '經濟' },
    { id: 9, word: 'factory', content: '工廠' },
    { id: 10, word: 'growth', content: '成長' },
    { id: 11, word: 'hospital', content: '醫院' },
    { id: 12, word: 'industry', content: '產業' },
    { id: 13, word: 'journey', content: '旅程' },
    { id: 14, word: 'knowledge', content: '知識' },
    { id: 15, word: 'leadership', content: '領導力' },
    { id: 16, word: 'market', content: '市場' },
    { id: 17, word: 'network', content: '網路' },
    { id: 18, word: 'opportunity', content: '機會' },
    { id: 19, word: 'product', content: '產品' },
    { id: 20, word: 'quality', content: '品質' },
    { id: 21, word: 'report', content: '報告' },
    { id: 22, word: 'service', content: '服務' },
    { id: 23, word: 'technology', content: '科技' }
];

/**
 * Session 隨機抽取演算法（多字母分散抽樣）
 */
class SessionManager {
    static shuffle(array) {
        const copy = [...array];
        for (let i = copy.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [copy[i], copy[j]] = [copy[j], copy[i]];
        }
        return copy;
    }

    static pickSessionWords(allWords, masteredIds = new Set(), sessionSize = 10) {
        if (!allWords || allWords.length === 0) return [];

        const unmastered = allWords.filter(w => !masteredIds.has(w.id));
        const pool = unmastered.length >= sessionSize ? unmastered : allWords;

        // 依照首字母分組
        const buckets = {};
        for (const card of pool) {
            const firstChar = (card.word[0] || '').toUpperCase();
            if (!buckets[firstChar]) buckets[firstChar] = [];
            buckets[firstChar].push(card);
        }

        // 隨機打亂首字母
        const availableLetters = this.shuffle(Object.keys(buckets));
        const selected = [];
        const usedWords = new Set();

        // 優先從不同字母中各挑選 1 個單字
        for (const letter of availableLetters) {
            if (selected.length >= sessionSize) break;
            const letterPool = buckets[letter];
            if (letterPool && letterPool.length > 0) {
                const randomCard = letterPool[Math.floor(Math.random() * letterPool.length)];
                if (!usedWords.has(randomCard.id)) {
                    selected.push(randomCard);
                    usedWords.add(randomCard.id);
                }
            }
        }

        // 不足則隨機補齊
        if (selected.length < sessionSize) {
            const remaining = this.shuffle(pool.filter(w => !usedWords.has(w.id)));
            for (const card of remaining) {
                if (selected.length >= sessionSize) break;
                selected.push(card);
            }
        }

        return this.shuffle(selected);
    }
}

/**
 * 打卡服務類別 (CheckInService)
 */
class CheckInService {
    static getTodayStr(date = new Date()) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
    }

    static calculateStreak(historyDates, todayStr = this.getTodayStr()) {
        if (!historyDates || historyDates.length === 0) return 0;
        const set = new Set(historyDates);

        let streak = 0;
        let checkDate = new Date(todayStr);

        if (!set.has(todayStr)) {
            checkDate.setDate(checkDate.getDate() - 1);
        }

        while (true) {
            const dateStr = this.getTodayStr(checkDate);
            if (set.has(dateStr)) {
                streak++;
                checkDate.setDate(checkDate.getDate() - 1);
            } else {
                break;
            }
        }

        return streak;
    }
}

console.log('=== 開始執行 Session 多元字母隨機抽取與打卡單元測試 ===');

// 測試 1：單字抽取必須涵蓋多個不同首字母，絕非連續 A 開頭
{
    const session = SessionManager.pickSessionWords(mockAlphabetVocabulary, new Set(), 10);
    assert.strictEqual(session.length, 10, 'Session 單字量應為 10 個');

    const firstLetters = session.map(w => w.word[0].toUpperCase());
    const uniqueLetters = new Set(firstLetters);
    
    console.log('抽取的 10 個單字:', session.map(w => w.word).join(', '));
    console.log('包含的首字母:', Array.from(uniqueLetters).join(', '));

    // 10 個單字應至少涵蓋 8 個以上不同首字母
    assert.ok(uniqueLetters.size >= 8, `抽取的單字首字母應高度分散多樣（當前涵蓋 ${uniqueLetters.size} 個不同字母）`);
    console.log(`✓ 測試 1 通過：成功從不同字母隨機抽取（包含 ${uniqueLetters.size} 個不同開頭字母）`);
}

// 測試 2：優先排除已掌握單字
{
    const mastered = new Set([1, 2, 3, 4, 5]); // 前 5 個已掌握
    const session = SessionManager.pickSessionWords(mockAlphabetVocabulary, mastered, 10);
    
    assert.strictEqual(session.length, 10);
    const hasMastered = session.some(w => mastered.has(w.id));
    assert.strictEqual(hasMastered, false, '抽取的單字應完全排除已掌握清單');
    console.log('✓ 測試 2 通過：掌握單字避讓機制正常');
}

// 測試 3：連續打卡 Streak 計算邏輯
{
    const today = '2026-08-19';
    const history1 = ['2026-08-17', '2026-08-18', '2026-08-19'];
    assert.strictEqual(CheckInService.calculateStreak(history1, today), 3, '連續 3 天打卡');

    const history2 = ['2026-08-17', '2026-08-18'];
    assert.strictEqual(CheckInService.calculateStreak(history2, today), 2, '昨天有打卡，今日尚未打卡保持 2');

    const history3 = ['2026-08-15', '2026-08-16'];
    assert.strictEqual(CheckInService.calculateStreak(history3, today), 0, '中間中斷應歸零');

    console.log('✓ 測試 3 通過：連續打卡 Streak 邏輯計算準確');
}

console.log('=== 所有單元測試全數通過 ===');
