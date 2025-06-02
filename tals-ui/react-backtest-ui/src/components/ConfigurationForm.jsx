import { useState } from 'react';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardHeader,
  Typography,
  TextField,
  FormControlLabel,
  Checkbox,
  Button,
  Box,
} from '@mui/material';

export default function ConfigurationForm({ onBacktestComplete }) {
  const [form, setForm] = useState({
    equities_per_firm: 1,
    number_of_firms: 5,
    selection_type_top: true,
    relative_weight: true,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const params = {
        ...form,
        equities_per_firm: parseInt(form.equities_per_firm),
        number_of_firms: parseInt(form.number_of_firms),
      };
      const existsResponse = await axios.get(import.meta.env.VITE_API_URL + '/conf-exists', { params });
      const { exists, id: configId } = existsResponse.data;

      if (exists) {
        const readyResponse = await axios.get(import.meta.env.VITE_API_URL + '/conf-ready', {
          params: { conf_id: configId },
        });

        if (readyResponse.data.ready) {
          onBacktestComplete(configId);
          return;
        } else {
          alert('Backtest is already running. Please try again later.');
        }
      } else {
        await axios.post(import.meta.env.VITE_API_URL + '/run-backtest', params);
        alert('Backtest started. Please wait and try again shortly.');
      }
    } catch (error) {
      console.error('Error during backtest submission:', error);
      alert('Something went wrong. Check the console.');
    }
  };

  return (
    <Box display="flex" justifyContent="center" mt={4}>
      <Card sx={{ height: '100%', width: '100%',display: 'flex', flexDirection: 'column', minHeight: '60vh' }}>
        <CardHeader title="Configuration" titleTypographyProps={{ variant: 'h6', fontWeight: 600, sx: { fontFamily: 'Inter, sans-serif' }}}/>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <Box mb={2}>
              <TextField
                fullWidth
                label="Equities per Firm"
                type="number"
                name="equities_per_firm"
                value={form.equities_per_firm}
                onChange={handleChange}
              />
            </Box>

            <Box mb={2}>
              <TextField
                fullWidth
                label="Number of Firms"
                type="number"
                name="number_of_firms"
                value={form.number_of_firms}
                onChange={handleChange}
              />
            </Box>

            <Box mb={2}>
              <FormControlLabel
                control={
                  <Checkbox
                    name="selection_type_top"
                    checked={form.selection_type_top}
                    onChange={handleChange}
                  />
                }
                label="Selection Type Top"
              />
            </Box>

            <Box mb={2}>
              <FormControlLabel
                control={
                  <Checkbox
                    name="relative_weight"
                    checked={form.relative_weight}
                    onChange={handleChange}
                  />
                }
                label="Relative Weight"
              />
            </Box>

            <Button type="submit" variant="contained" fullWidth>
              Run Backtest
            </Button>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
}
