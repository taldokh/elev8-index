import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

export default function IndexGraph({ configId, refreshTrigger }) {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (!configId) return;

    axios
      .get(import.meta.env.VITE_API_URL + '/index-points', {
        params: { config_id: configId },
      })
      .then((res) => {
        console.log(res)
        const data = res.data;
        const chartData = {
          labels: data.map((point) => point.market_date),
          datasets: [
            {
              label: 'Index Value',
              data: data.map((point) => point.day_end_points),
              borderColor: 'blue',
              backgroundColor: 'rgba(0, 0, 255, 0.2)',
              fill: true,
              tension: 0.3,
            },
            {
              label: 'S&P 500',
              data: data.map((point) => point.sp_index),
              borderColor: 'red',
              borderDash: [5, 5],
              fill: false,
              tension: 0.3,
            },
          ],
        };

        setChartData(chartData);
      })
      .catch((error) => {
        console.error('Error fetching index data:', error);
      });
  }, [configId, refreshTrigger]);

  return (
    <div className="chart-container">
      <h2>Index Graph</h2>
      <div className="chart-wrapper">
        {chartData ? (
          <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false, animation: false }} />
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
  );
}
