/**
 * 模組名稱：test_dialogue_prompt.js
 * 測試說明：驗證 AI 語音對話提示詞生成服務 (DialoguePromptService) 的結構與內容
 */

const assert = require('assert');

/**
 * AI 對話提示詞生成服務 (DialoguePromptService)
 * 遵循 Single Responsibility Principle (SRP)
 */
class DialoguePromptService {
    /**
     * 生成用於 ChatGPT / Gemini 實時語音對話的提示詞
     * @param {string} word - 目標單字
     * @param {string} sentence - 英文例句
     * @param {string} zhTranslation - 中文翻譯 (選填)
     * @returns {string} 格式化後的 Prompt
     */
    static generatePrompt(word, sentence, zhTranslation = '') {
        if (!word || !sentence) {
            throw new Error('單字與例句不可為空');
        }

        const cleanWord = word.trim();
        const cleanSentence = sentence.trim();
        const transText = zhTranslation ? ` (${zhTranslation.trim()})` : '';

        return `請扮演一位友善的朋友，跟我進行一場輕鬆自然、專注於口語應用的英文語音對話練習。

【本次練習主題】
• 目標單字：${cleanWord}
• 參考例句：${cleanSentence}${transText}

【對話規則】
1. 請以朋友般輕鬆自然的口吻，圍繞這個單字和例句所代表的情境，向我提出 3 個相關的口語問題進行問答練習。
2. 請務必「一次只提出 1 個問題」，等我用語音回答後，再接續下一個問題，絕不要一次列出所有問題。
3. 每次你的回覆請精簡在 1~2 句話，適合實時語音交流，避免冗長書面語。
4. 當我回答後，若我的英文有明顯表達錯誤，請用友善的方式順帶給予 1 句簡短的口語修飾建議，然後繼續我們的對話。
5. 現在，請直接用全英文向我打招呼，並提出第 1 個問題開始對話！`;
    }
}

console.log('=== 開始執行 AI 語音對話提示詞單元測試 ===');

// 測試 1: 正常生成提示詞
{
    const word = 'collaborate';
    const sentence = 'The two teams will collaborate on the new project.';
    const translation = '這兩個團隊將在新項目上進行合作。';

    const prompt = DialoguePromptService.generatePrompt(word, sentence, translation);

    assert.ok(prompt.includes('目標單字：collaborate'), '應包含目標單字');
    assert.ok(prompt.includes('The two teams will collaborate on the new project.'), '應包含英文例句');
    assert.ok(prompt.includes('這兩個團隊將在新項目上進行合作。'), '應包含中文翻譯');
    assert.ok(prompt.includes('提出 3 個相關的口語問題'), '應包含 3 個問題設定');
    assert.ok(prompt.includes('一次只提出 1 個問題'), '應設定逐一提問規則');
    assert.ok(prompt.includes('1~2 句話'), '應設定適合語音的簡短回覆規則');

    console.log('✓ 測試 1 通過：提示詞完整包含角色、單字、例句與互動規則');
}

// 測試 2: 無中文翻譯時的 fallback
{
    const word = 'innovate';
    const sentence = 'We need to innovate to stay competitive.';

    const prompt = DialoguePromptService.generatePrompt(word, sentence);

    assert.ok(prompt.includes('目標單字：innovate'));
    assert.ok(prompt.includes('We need to innovate to stay competitive.'));
    assert.ok(!prompt.includes('()'), '不應出現空的括號');

    console.log('✓ 測試 2 通過：無翻譯時優雅處理');
}

// 測試 3: 空值防呆檢查
{
    assert.throws(() => {
        DialoguePromptService.generatePrompt('', '');
    }, /單字與例句不可為空/, '空值應拋出錯誤');

    console.log('✓ 測試 3 通過：空值防呆驗證正常');
}

console.log('=== AI 語音對話提示詞所有單元測試全數通過！ ===');
