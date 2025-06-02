import React, { useState } from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Box,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const Section = ({ title, children }) => (
  <Accordion disableGutters elevation={1} sx={{ borderRadius: 2, mb: 2 }}>
    <AccordionSummary expandIcon={<ExpandMoreIcon />} sx={{ bgcolor: '#f9f9fb' }}>
      <Typography variant="h6" sx={{ fontWeight: 600 }}>
        {title}
      </Typography>
    </AccordionSummary>
    <AccordionDetails>
      <Typography variant="body1" sx={{ color: '#444', lineHeight: 1.8 }}>
        {children}
      </Typography>
    </AccordionDetails>
  </Accordion>
);

export default function About() {
  return (
    <Box>
      <Section title="Why Elev8?">
        Elev8 is designed to capture the collective wisdom of the most successful investment firms.
        By tracking the top holdings of elite hedge funds through their 13F filings, we construct
        an index that mirrors the behavior of institutional giants. This approach offers everyday
        investors a data-driven, research-backed strategy aligned with the world’s top capital allocators.
      </Section>

      <Section title="Description">
        The Elev8 Index is rebalanced quarterly using the most recent 13F filings. We analyze top equity
        positions from leading hedge funds, filtering for significant holdings to create a diversified
        yet targeted index. Our goal is to provide a transparent, rules-based strategy offering exposure
        to stocks selected by high-conviction institutional investors.
      </Section>

      <Section title="Allocation Strategy">
        <Box component="div" sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography>
            Our index construction begins with <strong>13F filings</strong>, offering a quarterly snapshot
            of institutional holdings. Users define how many firms and equities per firm to include.
          </Typography>

          <Typography>
            <strong>Selection Type:</strong>
            <ul>
              <li><strong>Top:</strong> Highest-weighted equities in each firm's portfolio.</li>
              <li><strong>Tercile:</strong> Picks stocks evenly across distribution. E.g., 1st, 4th, 7th by weight if selecting 3 of 9.</li>
            </ul>
          </Typography>

          <Typography>
            <strong>Weighting Method:</strong>
            <ul>
              <li><strong>Relative Weight:</strong> Based on portfolio percentage.</li>
              <li><strong>Equal Weight:</strong> All selected equities from a firm have equal weight.</li>
            </ul>
          </Typography>

          <Typography>
            Regardless of the strategy, each firm’s contribution to the index remains equally weighted.
          </Typography>
        </Box>
      </Section>
    </Box>
  );
}
