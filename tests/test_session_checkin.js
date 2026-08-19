/**
 * 模組名稱：test_session_checkin.js
 * 測試說明：驗證單字隨機抽取、每日 Session 10 字管理與連續打卡 Streak 演算法
 */

const assert = require('assert');

// 模擬單字庫（按字母順序）
const mockVocabulary = [
    { id: 1, word: 'ability', content: '能力' },
    { id: 2, word: 'abroad', content: '在國外' },
    { id: 3, word: 'absence', content: '缺席' },
    { id: 4, word: 'absolute', content: '絕對的' },
    { id: 5, word: 'absorb', content: '吸收' },
    { id: 6, word: 'abstract', content: '抽象的' },
    { id: 7, word: 'academic', content: '學術的' },
    { id: 8, word: 'accelerate', content: '加速' },
    { id: 9, word: 'accept', content: '接受' },
    { id: 10, word: 'access', content: '進入' },
    { id: 11, word: 'accident', content: '意外' },
    { id: 12, word: 'accommodate', content: '容納' },
    { id: 13, word: 'accompany', content: '陪同' },
    { id: 14, word: 'accomplish', content: '完成' },
    { id: 15, word: 'account', content: '帳戶' },
    { id: 16, word: 'accumulate', content: '累積' },
    { id: 17, word: 'accurate', content: '精確的' },
    { id: 18, word: 'accuse', content: '指控' },
    { id: 19, word: 'achieve', content: '達到' },
    { id: 20, word: 'acquire', content: '獲得' }
];

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

        // 如果今天還沒打卡，檢查昨天是否打卡延續
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

/**
 * Session 隨機抽取演算法
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
        
        // 優先抽取尚未掌握的單字
        const unmastered = allWords.filter(w => !masteredIds.has(w.id));
        const pool = unmastered.length >= sessionSize ? unmastered : allWords;
        
        const shuffled = this.shuffle(pool);
        return shuffled.slice(0, Math.min(sessionSize, shuffled.length));
    }
}

console.log('=== 開始執行 Session 與打卡機制單元測試 ===');

// 測試 1：單字抽取必須為隨機且不按字母順序排列
{
    const session1 = SessionManager.pickSessionWords(mockVocabulary, new Set(), 10);
    const session2 = SessionManager.pickSessionWords(mockVocabulary, new Set(), 10);

    assert.strictEqual(session1.length, 10, 'Session 單字量應為 10 個');
    assert.strictEqual(session2.length, 10, 'Session 單字量應為 10 個');

    const isSequential1 = session1.every((w, idx) => idx === 0 || w.id > session1[idx - 1].id);
    console.log('Session 1 抽取的單字:', session1.map(w => w.word).join(', '));
    assert.strictEqual(isSequential1, false, '抽取的單字不應該完全按字母序排列');
    console.log('✓ 測試 1 通過：隨機抽取單字成功，非字母順序排列');
}

// 測試 2：優先排除已掌握單字
{
    const mastered = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]); // 前 10 個已掌握
    const session = SessionManager.pickSessionWords(mockVocabulary, mastered, 10);
    
    assert.strictEqual(session.length, 10);
    const hasMastered = session.some(w => mastered.has(w.id));
    assert.strictEqual(hasMastered, false, '抽取的單字應完全排除已掌握清單');
    console.log('✓ 測試 2 通過：掌握單字避讓機制正常');
}

// 測試 3：連續打卡 Streak 計算邏輯
{
    const today = '2026-08-19';
    // 連續 3 天 (8/17, 8/18, 8/19)
    const history1 = ['2026-08-17', '2026-08-18', '2026-08-19'];
    assert.strictEqual(CheckInService.calculateStreak(history1, today), 3, '連續 3 天打卡');

    // 昨天有打，今天尚未打 (8/17, 8/18)，Streak 應保持為 2
    const history2 = ['2026-08-17', '2026-08-18'];
    assert.strictEqual(CheckInService.calculateStreak(history2, today), 2, '昨天有打卡，今日尚未打卡保持 2');

    // 斷卡情況 (8/15, 8/16)，中間空掉，Streak 應歸 0
    const history3 = ['2026-08-15', '2026-08-16'];
    assert.strictEqual(CheckInService.calculateStreak(history3, today), 0, '中間中斷應歸零');

    console.log('✓ 測試 3 通過：連續打卡 Streak 邏輯計算準確');
}

console.log('=== 所有 Session 與打卡單元測試全數通過 ===');
