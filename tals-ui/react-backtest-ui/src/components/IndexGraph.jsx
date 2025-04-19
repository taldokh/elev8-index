import { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function IndexGraph({ refreshTrigger }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/index-points')
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, [refreshTrigger]);

  const chartData = {
    labels: data.map(point => point.market_date),
    datasets: [
      {
        label: 'Start Points',
        data: data.map(point => point.day_start_points),
        borderColor: 'blue',
      },
      {
        label: 'End Points',
        data: data.map(point => point.day_end_points),
        borderColor: 'green',
      }
    ]
  };

  return (
    <div>
      <h2>Index Performance</h2>
      <Line data={chartData} />
    </div>
  );
}
