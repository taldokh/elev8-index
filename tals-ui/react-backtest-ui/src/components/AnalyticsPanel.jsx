import { useEffect, useState } from 'react';
import './AnalyticsPanel.css';

export default function AnalyticsPanel({ configId }) {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    if (!configId) return;

    fetch(import.meta.env.VITE_API_URL + `/index-analytics?config_id=${configId}`)
      .then((res) => res.json())
      .then(setAnalytics)
      .catch((err) => console.error('Failed to fetch analytics:', err));
  }, [configId]);

  if (!analytics) return null;
  return (
    <div className="analytics-panel">
      <h2>Performance Analytics</h2>
      <ul>
        <li><strong>Sharpe Ratio:</strong> {analytics.sharpe_ratio.toFixed(2)}</li>
        <li><strong>Max Drawdown:</strong> {analytics.max_drawdown.toFixed(2)}%</li>
        <li><strong>Annualized Return:</strong> {analytics.annualized_return.toFixed(2)}%</li>
        <li><strong>Annualized Volatility:</strong> {analytics.annualized_volatility.toFixed(2)}%</li>
        <li><strong>Total Return:</strong> {analytics.total_return.toFixed(2)}%</li>
      </ul>
    </div>
  );
}
