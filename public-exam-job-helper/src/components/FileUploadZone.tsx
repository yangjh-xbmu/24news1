import React, { useCallback, useState } from 'react';
import { parseExcelFile } from '../lib/excelParser';
import type { ExcelData } from '../types';
import { cn } from '../lib/utils';

interface FileUploadZoneProps {
  onFileParsed: (data: ExcelData) => void;
}

export function FileUploadZone({ onFileParsed }: FileUploadZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isParsing, setIsParsing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const processFile = async (file: File) => {
    if (!file) return;
    
    // 简单验证文件类型
    const validTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
      'application/vnd.ms-excel', // .xls
    ];
    // 有些系统可能 mime type 不准确，也可以校验后缀
    const isExcel = validTypes.includes(file.type) || /\.(xlsx|xls)$/i.test(file.name);

    if (!isExcel) {
      setError('请上传 Excel 文件 (.xlsx 或 .xls)');
      return;
    }

    setIsParsing(true);
    setError(null);
    setFileName(file.name);

    try {
      const data = await parseExcelFile(file);
      onFileParsed(data);
    } catch (err) {
      console.error(err);
      setError('文件解析失败，请检查文件格式是否正确');
      setFileName(null);
    } finally {
      setIsParsing(false);
    }
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    processFile(file);
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          "relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ease-in-out",
          isDragging 
            ? "border-primary bg-primary/5 scale-[1.02]" 
            : "border-gray-300 hover:border-primary/50 hover:bg-gray-50",
          fileName ? "bg-green-50 border-green-200" : ""
        )}
      >
        <input
          type="file"
          accept=".xlsx,.xls"
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          onChange={handleFileSelect}
          disabled={isParsing}
        />
        
        <div className="flex flex-col items-center justify-center space-y-4">
          {isParsing ? (
            <div className="animate-pulse flex flex-col items-center">
              <div className="h-10 w-10 border-4 border-primary border-t-transparent rounded-full animate-spin mb-2"></div>
              <p className="text-primary font-medium">正在解析文件...</p>
            </div>
          ) : fileName ? (
            <div className="flex flex-col items-center">
              <div className="h-12 w-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-2">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-green-800 font-medium text-lg">{fileName}</p>
              <p className="text-green-600 text-sm mt-1">点击或拖拽可更换文件</p>
            </div>
          ) : (
            <>
              <div className="h-16 w-16 bg-primary/10 text-primary rounded-full flex items-center justify-center">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <p className="text-lg font-medium text-text-main">
                  点击或拖拽上传 Excel 文件
                </p>
                <p className="text-sm text-text-secondary mt-1">
                  支持 .xlsx, .xls 格式
                </p>
              </div>
            </>
          )}
        </div>
      </div>
      
      {error && (
        <div className="mt-4 p-3 bg-red-50 text-red-700 rounded-md flex items-center text-sm border border-red-100">
          <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      )}
    </div>
  );
}
