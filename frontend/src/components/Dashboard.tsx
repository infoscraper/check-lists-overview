import { useState, useEffect, useMemo, useCallback } from 'react';
import { dashboardApi } from '../api/dashboard';
import { recordsApi } from '../api/records';
import { checklistsApi } from '../api/checklists';
import { DashboardSummary, ProcessRecord, STATUS_COLORS, TABLE_SOURCE_NAMES, TableSource, Checklist } from '../types';
import './Dashboard.css';

const Dashboard = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [records, setRecords] = useState<ProcessRecord[]>([]);
  const [checklists, setChecklists] = useState<Checklist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Создаем мапу названий чек-листов
  const checklistNamesMap = useMemo(() => {
    const map: Record<string, string> = {};
    checklists.forEach(checklist => {
      map[checklist.table_source] = checklist.name;
    });
    return map;
  }, [checklists]);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [summaryData, recordsData, checklistsData] = await Promise.all([
        dashboardApi.getSummary(),
        recordsApi.getRecords({ limit: 1000 }),
        checklistsApi.getChecklists(true), // Включая виртуальные
      ]);
      
      setSummary(summaryData);
      setRecords(recordsData.records);
      setChecklists(checklistsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка загрузки данных');
      console.error('Dashboard fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    
    // Обновляем данные каждые 30 секунд
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const renderFrameworkCard = useCallback((source: TableSource, stats: any) => {
    // Получаем записи для этого источника
    const sourceRecords = records.filter(r => r.table_source === source);
    
    // Вычисляем процент выполнения (только завершенные статусы)
    const completed = stats.completed || 0;
    const total = stats.total || 1;
    const completionPercent = total > 0 ? Math.round((completed / total) * 100) : 0;

    // Получаем название чек-листа из мапы или используем table_source как fallback
    const checklistName = checklistNamesMap[source] || source;

    // Цвета для квадратиков (как на скриншоте)
    const getSquareColor = (status: string) => {
      if (status === 'Выполнено' || status === 'Успешно') return '#22c55e'; // dark green (completed/passing)
      if (status === 'В работе') return '#3b82f6'; // blue (in progress/assigned)
      if (status === 'Не успешно') return '#f97316'; // orange (at risk/failed)
      return '#e2e8f0'; // light gray (unstarted/unassigned)
    };

    return (
      <div key={source} className="framework-card">
        <div className="framework-header">
          <div className="framework-title-group">
            <span className="framework-label">Название чек-листа</span>
            <h3 className="framework-name">{checklistName}</h3>
          </div>
        </div>

        <div className="framework-progress-grid">
          {sourceRecords.map((record) => {
            const color = getSquareColor(record.status);
            const tooltip = `${record.process_name} - ${record.status}`;
            
            return (
              <div
                key={record.id}
                className="framework-square"
                style={{ backgroundColor: color }}
                title={tooltip}
              />
            );
          })}
        </div>

        <div className="framework-metrics">
          <div className="framework-metric">
            <span className="metric-value">{completed}/{total}</span>
            <span className="metric-label">controls passing</span>
          </div>
          <div className="framework-metric">
            <span className="metric-label">Выполнено</span>
            <span className="metric-value">{completionPercent}%</span>
          </div>
        </div>
      </div>
    );
  }, [records, checklistNamesMap]);

  if (loading) {
    return <div className="dashboard-loading">Загрузка...</div>;
  }

  if (error) {
    return <div className="dashboard-error">Ошибка: {error}</div>;
  }

  if (!summary) {
    return <div className="dashboard-error">Нет данных</div>;
  }

  // Вычисляем количество чек-листов (источников с данными)
  const activeFrameworksCount = Object.keys(summary.by_source).length;
  
  // Вычисляем requirements met (можно использовать completed или другую метрику)
  const requirementsMet = summary.completed;

  return (
    <div className="dashboard">
      {/* Верхняя секция - Обзор */}
      <div className="dashboard-overview">
        <div className="overview-header">
          <h1 className="overview-title">Пользовательское тестирование процессов ЦФТ-Банк</h1>
        </div>

        <div className="overview-metrics">
          <div className="overview-metric-card">
            <div className="metric-label-ru">Общий прогресс</div>
            <div className="metric-value-large">
              {summary.progress_percent.toFixed(0)}% - {summary.completed}/{summary.total_records}
            </div>
          </div>

          <div className="overview-metric-card">
            <div className="metric-label-ru">Кол-во чек-листов</div>
            <div className="metric-value-large">
              {activeFrameworksCount} controls
            </div>
          </div>

          <div className="overview-metric-card">
            <div className="metric-label-ru">Выполнено</div>
            <div className="metric-value-large">
              {requirementsMet}/{summary.total_records}
            </div>
          </div>
        </div>
      </div>

      {/* Секция Active Frameworks */}
      <div className="active-frameworks-section">
        <div className="section-header">
          <div>
            <h2 className="section-title">Обзор прогресса по тестированию операций в ЦФТ-Банк</h2>
          </div>
        </div>

        <div className="frameworks-grid">
          {Object.entries(summary.by_source).map(([source, stats]) => 
            renderFrameworkCard(source as TableSource, stats)
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

