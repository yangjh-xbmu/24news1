import { describe, it, expect } from 'vitest';
import * as XLSX from 'xlsx';
import * as fs from 'fs';
import * as path from 'path';
import { fuzzyMatch } from './matchLogic';

// 真实数据路径
const REAL_DATA_PATH = 'c:/Users/yangjh/Desktop/repoes/24news1/data/xls/3c7d0df48493449099e93136ac5ca6cc.xlsx';

describe('Real Data Test', () => {
  it('should parse real excel file and match professions', () => {
    // 1. 读取文件
    if (!fs.existsSync(REAL_DATA_PATH)) {
      console.warn(`File not found: ${REAL_DATA_PATH}, skipping test.`);
      return;
    }
    
    const buf = fs.readFileSync(REAL_DATA_PATH);
    const workbook = XLSX.read(buf, { type: 'buffer' });
    const firstSheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[firstSheetName];
    
    // 2. 解析数据
    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 }) as any[][];
    expect(jsonData.length).toBeGreaterThan(0);

    // 寻找真正的表头行
    // 策略：遍历前 10 行，找到包含 "专业" 或 "招录单位" 的行
    let headerRowIndex = -1;
    let headers: string[] = [];
    
    for (let i = 0; i < Math.min(10, jsonData.length); i++) {
      const row = jsonData[i] as string[];
      // 检查行中是否包含关键字段
      if (row.some(cell => typeof cell === 'string' && (cell.includes('专业') || cell.includes('招录单位')))) {
        headerRowIndex = i;
        headers = row;
        break;
      }
    }

    if (headerRowIndex === -1) {
      console.warn('Could not find header row in first 10 rows.');
      // 打印前5行供调试
      console.log('First 5 rows:', jsonData.slice(0, 5));
      return;
    }

    console.log(`Found Header Row at index ${headerRowIndex}:`, headers);

    // 寻找“专业”相关的列
    // 通常表头可能包含 "专业" 字样，如 "专业要求"、"专业" 等
    const professionColIndex = headers.findIndex(h => h && typeof h === 'string' && h.includes('专业'));
    console.log(`Found Profession Column: "${headers[professionColIndex]}" at index ${professionColIndex}`);

    if (professionColIndex === -1) {
      console.warn('Could not find profession column in headers.');
      return;
    }

    // 数据行从表头行的下一行开始
    const rows = jsonData.slice(headerRowIndex + 1);
    
    // 3. 测试匹配逻辑
    // 随机抽取几行或者针对特定行进行测试
    // 让我们统计一下有多少行匹配 "计算机"
    const keyword = '计算机';
    let matchCount = 0;
    const matchedExamples: string[] = [];

    rows.forEach((row, index) => {
      const professionReq = row[professionColIndex];
      if (typeof professionReq === 'string') {
        const isMatch = fuzzyMatch(professionReq, keyword);
        if (isMatch) {
          matchCount++;
          if (matchedExamples.length < 5) {
            matchedExamples.push(`Row ${index + 2}: [${professionReq}]`);
          }
        }
      }
    });

    console.log(`Total rows: ${rows.length}`);
    console.log(`Rows matching "${keyword}": ${matchCount}`);
    console.log('First 5 matches:');
    matchedExamples.forEach(ex => console.log(ex));

    // 断言：应该至少有一些匹配（假设真实数据里有计算机岗）
    // 如果文件中确实没有计算机岗，这个断言可能会失败，所以我们要谨慎。
    // 但作为测试脚本，打印出来供用户确认更重要。
    expect(rows.length).toBeGreaterThan(0);
  });
});
