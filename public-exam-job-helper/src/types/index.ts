export interface JobPosition {
  id: string;
  [key: string]: string | number | undefined;
}

export interface ExcelData {
  headers: string[];
  rows: any[];
}
