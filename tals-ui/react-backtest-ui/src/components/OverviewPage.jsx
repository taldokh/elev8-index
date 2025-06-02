import React from 'react';
import Overview from './Overview';
import QuickFacts from './QuickFacts';
import { Container, Typography, Box, Grid } from '@mui/material';
import analyticsIllustration from './../assets/undraw_investing.svg';
import dataTrendsIllustration from './../assets/undraw_segment-analysis.svg';

function OverviewPage() {
  return (
    <Container maxWidth="lg" sx={{ py: 6, px: { xs: 2, md: 6 } }}>
      <Typography variant="h4" fontWeight={700} gutterBottom textAlign="center">
        About Elev8
      </Typography>

      {/* Overview + Illustration */}
      <Grid container spacing={4} alignItems="center" sx={{ mb: 8 }}>
        <Grid
          item
          xs={12}
          md={6}
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            px: { md: 4 },
          }}
        >
          <Box sx={{ maxWidth: 600 }}>
            <Overview />
          </Box>
        </Grid>
        <Grid
          item
          xs={12}
          md={6}
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Box
            component="img"
            src={analyticsIllustration}
            alt="Analytics illustration"
            sx={{
              width: '100%',
              maxWidth: 600,
              maxHeight: 400,
              objectFit: 'contain',
            }}
          />
        </Grid>
      </Grid>

      {/* QuickFacts + Illustration */}
      <Grid container spacing={4} alignItems="center">
        <Grid
          item
          xs={12}
          md={6}
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <Box
            component="img"
            src={dataTrendsIllustration}
            alt="Data trends illustration"
            sx={{
              width: '100%',
              maxWidth: 600,
              maxHeight: 400,
              objectFit: 'contain',
            }}
          />
        </Grid>
        <Grid
          item
          xs={12}
          md={6}
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            px: { md: 4 },
          }}
        >
          <Box sx={{ maxWidth: 600 }}>
            <QuickFacts />
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
}

export default OverviewPage;
