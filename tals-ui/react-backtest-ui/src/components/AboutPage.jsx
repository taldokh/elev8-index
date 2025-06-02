import React from 'react';
import About from '../components/About';
import { Container, Typography, Box } from '@mui/material';

function AboutPage() {
  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        About Elev8
      </Typography>
      <Box mt={4}>
        <About />
      </Box>
    </Container>
  );
}

export default AboutPage;
