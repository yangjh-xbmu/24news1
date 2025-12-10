import { useState } from 'react'
import { FileUploadZone } from './components/FileUploadZone'
import type { ExcelData } from './types'

function App() {
  const [excelData, setExcelData] = useState<ExcelData | null>(null);

  const handleFileParsed = (data: ExcelData) => {
    console.log('Parsed data:', data);
    setExcelData(data);
  };

  return (
    <div className="min-h-screen bg-background text-text-main p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <header className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-text-main">公考职位快筛助手</h1>
          <p className="text-text-secondary">零部署、高隐私、极速匹配你的心仪岗位</p>
        </header>

        <main className="space-y-8">
          <section className="bg-white rounded-xl shadow-sm border border-primary-light/20 p-6 md:p-10">
            <h2 className="text-xl font-semibold mb-6 flex items-center">
              <span className="bg-primary/10 text-primary w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm">1</span>
              上传职位表
            </h2>
            <FileUploadZone onFileParsed={handleFileParsed} />
          </section>

          {excelData && (
            <section className="bg-white rounded-xl shadow-sm border border-primary-light/20 p-6 md:p-10 animate-fade-in">
              <h2 className="text-xl font-semibold mb-6 flex items-center">
                <span className="bg-primary/10 text-primary w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm">2</span>
                数据预览 (前5行)
              </h2>
              <div className="overflow-x-auto">
                <table className="min-w-full text-sm text-left">
                  <thead className="bg-gray-50 text-text-secondary font-medium">
                    <tr>
                      {excelData.headers.map((header, idx) => (
                        <th key={idx} className="px-4 py-3 border-b whitespace-nowrap">{header}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {excelData.rows.slice(0, 5).map((row) => (
                      <tr key={row.id} className="hover:bg-gray-50">
                        {excelData.headers.map((header, idx) => (
                          <td key={idx} className="px-4 py-3 max-w-[200px] truncate" title={String(row[header])}>
                            {row[header]}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="mt-4 text-center text-sm text-text-secondary">
                共解析 {excelData.rows.length} 条数据
              </div>
            </section>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
