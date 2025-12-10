import { describe, it, expect } from 'vitest';
import { fuzzyMatch, defaultProfessionMap } from './matchLogic';

describe('fuzzyMatch', () => {
  it('should match when post requirement directly contains keyword (Direction A)', () => {
    const postReq = '新闻传播学类、历史学';
    const keyword = '新闻';
    expect(fuzzyMatch(postReq, keyword)).toBe(true);
  });

  it('should match multiple keywords split by separators', () => {
    const postReq = '计算机科学与技术';
    const keyword = '英语;计算机';
    expect(fuzzyMatch(postReq, keyword)).toBe(true);
  });

  it('should match when user input implies a super category required by post (Direction B)', () => {
    // Map has "新闻传播学类": ["新闻学", ...]
    const postReq = '新闻传播学类'; // Post asks for Super
    const keyword = '新闻学'; // User has Sub
    expect(fuzzyMatch(postReq, keyword)).toBe(true);
  });

  it('should not match unrelated professions', () => {
    const postReq = '计算机类';
    const keyword = '新闻学';
    expect(fuzzyMatch(postReq, keyword)).toBe(false);
  });

  it('should handle complex post requirements with multiple categories', () => {
    const postReq = '汉语言文学，新闻传播学类，哲学';
    const keyword = '新闻学'; // Should match via mapping to "新闻传播学类"
    expect(fuzzyMatch(postReq, keyword)).toBe(true);
  });

  it('should be case insensitive', () => {
    const postReq = 'Computer Science';
    const keyword = 'computer';
    expect(fuzzyMatch(postReq, keyword)).toBe(true);
  });

  it('should handle empty user query as match all', () => {
    expect(fuzzyMatch('Any', '')).toBe(true);
    expect(fuzzyMatch('Any', '   ')).toBe(true);
  });

  it('should handle empty post requirement as no match (unless query is empty)', () => {
    expect(fuzzyMatch('', 'Something')).toBe(false);
  });
});
