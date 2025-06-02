import { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import zoomPlugin from 'chartjs-plugin-zoom';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

import {
  Card,
  CardContent,
  CardHeader,
  Typography,
  Box,
  Button,
} from '@mui/material';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend, Filler, zoomPlugin);

export default function IndexGraph({ configId, refreshTrigger }) {
  const [chartData, setChartData] = useState(null);
  const chartRef = useRef(null); // For accessing the chart instance

  useEffect(() => {
    if (!configId) return;

    axios
      .get(import.meta.env.VITE_API_URL + '/index-points', {
        params: { config_id: configId },
      })
      .then((res) => {
        const data = res.data;
        const chartData = {
          labels: data.map((point) => point.market_date),
          datasets: [
            {
              label: 'Index Value',
              data: data.map((point) => point.day_end_points),
              borderColor: '#1976d2',
              backgroundColor: 'rgba(25, 118, 210, 0.2)',
              fill: true,
              tension: 0.4,
              pointRadius: 2,
              pointHoverRadius: 5,
            },
            {
              label: 'S&P 500',
              data: data.map((point) => point.sp_index),
              borderColor: '#e53935',
              borderDash: [5, 5],
              fill: false,
              tension: 0.4,
              pointRadius: 2,
              pointHoverRadius: 5,
            },
          ],
        };

        setChartData(chartData);
      })
      .catch((error) => {
        console.error('Error fetching index data:', error);
      });
  }, [configId, refreshTrigger]);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      tooltip: {
        mode: 'nearest',
        intersect: false,
      },
      legend: {
        position: 'bottom',
      },
      zoom: {
        pan: {
          enabled: true,
          mode: 'x',
        },
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
          },
          mode: 'x',
        },
        limits: {
          x: { min: 'original', max: 'original' },
          y: { min: 'original', max: 'original' },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Date',
        },
        ticks: {
          maxTicksLimit: 10,
        },
      },
      y: {
        title: {
          display: true,
          text: 'Index Points',
        },
      },
    },
  };

  const handleResetZoom = () => {
    if (chartRef.current) {
      chartRef.current.resetZoom();
    }
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center" mt={4}>
      <Card sx={{height: '100%', width: '100%', display: 'flex', flexDirection: 'column', minHeight: '60vh' }}>
        <CardHeader title="Index Graph" titleTypographyProps={{ variant: 'h6', fontWeight: 600, sx: { fontFamily: 'Inter, sans-serif' }}}/>
        <CardContent>
          {chartData ? (
            <>
              <Box height={400}>
                <Line ref={chartRef} data={chartData} options={chartOptions} />
              </Box>
              <Box display="flex" justifyContent="flex-end" mt={2}>
                <Button variant="outlined" onClick={handleResetZoom}>
                  Reset Zoom
                </Button>
              </Box>
            </>
          ) : (
            <Typography variant="body2">Loading...</Typography>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
