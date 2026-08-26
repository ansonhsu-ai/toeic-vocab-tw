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

                return `請扮演一位親切友善的朋友，跟我進行一場輕鬆有趣的英文即時語音口說練習。

【學習者程度與設定】
• 我的程度：小學六年級學生（詞彙量約 3000 字以內，CEFR A2 程度）。
• 語言難度：請使用「基礎 3000 常見單字」與「簡短清晰的日常句型」，絕不使用複雜長句或艱深文法。
• 語音語速：請將說話語速調整為平常語速的 85%（略慢節奏、發音清晰自然，讓學生能輕鬆聽懂並跟上）。

【本次練習主題】
• 目標單字：${cleanWord}
• 參考例句：${cleanSentence}${transText}

【對話規則】
1. 請圍繞這個單字與例句的情境（盡量貼近學生的校園生活、興趣愛好或日常經歷），向我提出 3 個簡單好回答的英文口語問題。
2. 每次對話「只問 1 個問題」，等我用語音回答後，再接續下一個問題，絕不要一次列出所有問題。
3. 你的每次回覆請精簡在 1~2 句話，語速保持在 85% 稍慢速度，語句口語自然，非常適合六年級學生的即時語音練習。
4. 若我的英文表達有誤，請先給予正面鼓勵，並直接示範 1 句簡單道地的說法（如 "You can also say: ..."），不使用複雜的文法術語。
5. 現在，請直接用親切、簡單、語速 85% 的英文向我打招呼，並提出第 1 個問題開始對話！`;
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
    assert.ok(prompt.includes('小學六年級學生'), '應包含六年級學生程度說明');
    assert.ok(prompt.includes('3000 字以內'), '應包含 3000 字以內詞彙限制');
    assert.ok(prompt.includes('85%'), '應包含 85% 語速設定');
    assert.ok(prompt.includes('提出 3 個簡單好回答的英文口語問題'), '應包含 3 個問題設定');
    assert.ok(prompt.includes('只問 1 個問題'), '應設定逐一提問規則');
    assert.ok(prompt.includes('1~2 句話'), '應設定適合語音的簡短回覆規則');

    console.log('✓ 測試 1 通過：提示詞完整包含六年級程度、3000字限制、85%語速、角色、單字、例句與互動規則');
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

// 測試 4: iOS 捷徑 URL 生成與編碼
{
    const shortcutName = 'TOEIC口說';
    const encodedName = encodeURIComponent(shortcutName);
    const shortcutsUrl = `shortcuts://run-shortcut?name=${encodedName}&input=clipboard`;

    assert.strictEqual(shortcutsUrl, 'shortcuts://run-shortcut?name=TOEIC%E5%8F%A3%E8%AA%AA&input=clipboard', 'iOS 捷徑 URL 格式與編碼需完全正確');
    console.log('✓ 測試 4 通過：iOS 捷徑 URL 生成與編碼正確');
}

console.log('=== AI 語音對話提示詞所有單元測試全數通過！ ===');
