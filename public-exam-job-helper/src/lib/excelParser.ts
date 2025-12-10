import * as XLSX from 'xlsx';
import type { ExcelData } from '../types';

/**
 * 解析 Excel 文件
 * @param file 用户上传的文件对象
 * @returns Promise<ExcelData> 解析后的数据
 */
export const parseExcelFile = (file: File): Promise<ExcelData> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target?.result as ArrayBuffer);
        const workbook = XLSX.read(data, { type: 'array' });
        
        // 取第一个工作表
        const firstSheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheetName];
        
        // 解析为 JSON，header: 1 表示按行数组返回，第一行为表头
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        if (jsonData.length === 0) {
          reject(new Error('Excel 文件为空'));
          return;
        }

        const headers = jsonData[0] as string[];
        // 移除表头行，保留数据行
        const rawRows = jsonData.slice(1) as any[][];

        // 将每行数据转换为对象，键为表头
        const rows = rawRows.map((row, index) => {
          const rowData: any = { id: `row-${index}` }; // 添加唯一ID
          headers.forEach((header, i) => {
            rowData[header] = row[i];
          });
          return rowData;
        });

        resolve({
          headers,
          rows,
        });
      } catch (error) {
        reject(error);
      }
    };

    reader.onerror = (error) => reject(error);
    reader.readAsArrayBuffer(file);
  });
};

/**
 * 提取指定列的唯一值
 * @param data Excel 数据行
 * @param key 要提取的列名（表头）
 * @returns 唯一值数组
 */
export const extractUniqueValues = (data: any[], key: string): string[] => {
  const values = new Set<string>();
  
  data.forEach(row => {
    const value = row[key];
    if (typeof value === 'string' && value.trim() !== '') {
      // 可能会有多个值用分隔符分开的情况？需求文档提到“自动提取‘专业要求’列的所有唯一值”，
      // 但通常下拉框是针对单元格内容的。如果单元格内容是“A类、B类”，是否要拆分？
      // 根据 FR2.1 “自动提取‘专业要求’列的所有唯一值”，这里暂且认为是提取单元格的完整文本作为选项。
      // 如果后续需要拆分单元格内容再去重，可以再调整。
      values.add(value.trim());
    }
  });

  return Array.from(values).sort();
};
