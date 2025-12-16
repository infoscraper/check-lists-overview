export interface ProcessRecord {
  id: string;
  process_name: string;
  product_type?: string;
  status: string;
  date_kb?: string;
  fio_customer?: string;
  date_bank_receipt?: string;
  fio_bank_officer?: string;
  process_number?: number;
  bank_employee_name?: string;
  comments?: string;
  table_source: string;
  import_date?: string;
  import_batch_id?: string;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProcessRecordCreate {
  process_name: string;
  product_type?: string;
  status: string;
  date_kb?: string;
  fio_customer?: string;
  date_bank_receipt?: string;
  fio_bank_officer?: string;
  process_number?: number;
  bank_employee_name?: string;
  comments?: string;
  table_source: string;
}

export interface ProcessRecordUpdate {
  process_name?: string;
  product_type?: string;
  status?: string;
  date_kb?: string;
  fio_customer?: string;
  date_bank_receipt?: string;
  fio_bank_officer?: string;
  process_number?: number;
  bank_employee_name?: string;
  comments?: string;
}

export interface DashboardSummary {
  total_records: number;
  completed: number;
  in_progress: number;
  not_started: number;
  progress_percent: number;
  by_source: Record<string, SourceSummary>;
}

export interface SourceSummary {
  total: number;
  completed: number;
  in_progress: number;
  not_started: number;
}

export interface ImportResponse {
  import_batch_id: string;
  total_rows: number;
  success_rows: number;
  error_rows: number;
  errors: ImportError[];
}

export interface ImportError {
  row: number;
  field: string;
  message: string;
}

export type TableSource =
  | 'safes_rental'
  | 'deposits_fl'
  | 'deposits_ul'
  | 'credits_fl'
  | 'payment_orders'
  | 'payment_processing';

export const TABLE_SOURCE_NAMES: Record<TableSource, string> = {
  safes_rental: 'Аренда Сейфов',
  deposits_fl: 'Депозиты ФЛ',
  deposits_ul: 'Депозиты ЮЛ',
  credits_fl: 'Кредиты ФЛ',
  payment_orders: 'Платежные поручения',
  payment_processing: 'Обработка платежей',
};

export const STATUS_COLORS: Record<string, string> = {
  'Выполнено': '#4ade80',
  'Успешно': '#4ade80',
  'В работе': '#facc15',
  'Не начато': '#d1d5db',
  'Не успешно': '#ef4444',
};

export interface Checklist {
  id: string;
  name: string;
  table_source: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ChecklistCreate {
  name: string;
}

