import { useEffect, useState } from 'react';
import {
  Card,
  CardHeader,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import PercentIcon from '@mui/icons-material/Percent';

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

  const items = [
    {
      label: 'Sharpe Ratio',
      value: analytics.sharpe_ratio.toFixed(2),
      icon: <QueryStatsIcon color="primary" />,
    },
    {
      label: 'Max Drawdown',
      value: `${analytics.max_drawdown.toFixed(2)}%`,
      icon: <TrendingDownIcon color="error" />,
    },
    {
      label: 'Annualized Return',
      value: `${analytics.annualized_return.toFixed(2)}%`,
      icon: <TrendingUpIcon color="success" />,
    },
    {
      label: 'Annualized Volatility',
      value: `${analytics.annualized_volatility.toFixed(2)}%`,
      icon: <ShowChartIcon color="secondary" />,
    },
    {
      label: 'Total Return',
      value: `${analytics.total_return.toFixed(2)}%`,
      icon: <PercentIcon color="primary" />,
    },
  ];

  return (
    <Card
      sx={{
        height: '100%',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        minHeight: '40vh',
      }}
    >
      <CardHeader
        title="Performance Analytics"
        titleTypographyProps={{ variant: 'h6', fontWeight: 600, sx: { fontFamily: 'Inter, sans-serif' }}}
      />
      <CardContent sx={{ pt: 0 }}>
        <List>
          {items.map(({ label, value, icon }) => (
            <ListItem
              key={label}
              sx={{
                '&:hover': { backgroundColor: 'rgba(0,0,0,0.03)', borderRadius: 2 },
              }}
            >
              <ListItemIcon>{icon}</ListItemIcon>
              <ListItemText
                primary={<Typography fontWeight={500}>{label}</Typography>}
                secondary={<Typography variant="body2" color="text.secondary">{value}</Typography>}
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}
