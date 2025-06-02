// QuickFacts.jsx
import React from 'react';
import { Box, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';

const facts = [
  { label: 'Weighting Method', value: 'Relative or equal weighted' },
  { label: 'Rebalancing Frequency', value: 'Quarterly in March, June, September, and December' },
  { label: 'Calculation Frequency', value: 'Real-time' },
  { label: 'Calculation Currencies', value: 'USD, AUD, BRL, CAD, CHF, EUR' },
  { label: 'Launch Date', value: 'Aug 15, 2013' },
  { label: 'Regulatory Authorization', value: 'European Union - Endorsed' },
  { label: 'Methodology', value: 'S&P U.S. Indices Methodology' },
];

export default function QuickFacts() {
  return (
    <Box sx={{ 
        mt: 4, 
        mb: 6, 
        display: 'flex',       // use flexbox
        flexDirection: 'column',
        alignItems: 'center'  // center horizontally
      }}>
      <Typography variant="h5" fontWeight={700} gutterBottom>
        Quick Facts
      </Typography>
      <List>
        {facts.map(({ label, value }) => (
          <React.Fragment key={label}>
            <ListItem disableGutters>
              <ListItemText
                primary={<Typography fontWeight={600}>{label}</Typography>}
                secondary={<Typography color="text.secondary">{value}</Typography>}
              />
            </ListItem>
            <Divider component="li" />
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
}
