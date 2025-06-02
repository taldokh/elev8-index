import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardHeader,
  Box,
  Typography,
  FormControl,
  Select,
  MenuItem,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableContainer,
  Paper,
} from '@mui/material';

function QuarterlyHoldings({ configId }) {
  const [data, setData] = useState({});
  const [quarters, setQuarters] = useState([]);
  const [selectedQuarter, setSelectedQuarter] = useState('');

  useEffect(() => {
    axios
      .get(import.meta.env.VITE_API_URL + `/equities-by-quarter?config_id=${configId}`)
      .then((res) => {
        setData(res.data);
        const q = Object.keys(res.data).sort(); // ISO strings sort chronologically
        setQuarters(q);
        if (q.length > 0) setSelectedQuarter(q[0]);
      })
      .catch((err) => console.error('Error fetching data:', err));
  }, [configId]);

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
      <CardHeader title="Equity Holdings" titleTypographyProps={{ variant: 'h6', fontWeight: 600, sx: { fontFamily: 'Inter, sans-serif' }}}/>

      <CardContent>
        {quarters.length > 0 ? (
          <>
            <Box mb={2} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography variant="body1" component="label" htmlFor="quarter-select">
                Select Quarter:
              </Typography>
              <FormControl size="small" sx={{ minWidth: 150 }}>
                <Select
                  id="quarter-select"
                  value={selectedQuarter}
                  onChange={(e) => setSelectedQuarter(e.target.value)}
                >
                  {quarters.map((q) => (
                    <MenuItem key={q} value={q}>
                      {q}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>

            <TableContainer component={Paper} elevation={1}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: 'bold' }}>Ticker</TableCell>
                    <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                      Weight (%)
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data[selectedQuarter]?.map((row) => (
                    <TableRow key={row.ticker} hover>
                      <TableCell>{row.ticker}</TableCell>
                      <TableCell align="right">{row.weight.toFixed(2)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </>
        ) : (
          <Typography>No holdings data found for this configuration.</Typography>
        )}
      </CardContent>
    </Card>
  );
}

export default QuarterlyHoldings;
