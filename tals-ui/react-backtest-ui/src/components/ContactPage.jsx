// src/pages/ContactPage.jsx
import React from 'react';
import { Container, Grid, Typography } from '@mui/material';
import TeamMemberCard from '../components/TeamMemberCard';

const team = [
  {
    image: '/images/john.jpg', // Replace with actual paths
    name: 'Tal Dokhanian',
    phone: '+1 (555) 123-4567',
    email: 'taldokh@gmail.com',
  },
  {
    image: '/images/emily.jpg',
    name: 'Eitan Aranovich',
    phone: '+1 (555) 234-5678',
    email: 'eitan5001100@gmail.com',
  },
  {
    image: '/images/daniel.jpg',
    name: 'Gilad Levovich',
    phone: '+1 (555) 345-6789',
    email: 'gilad.levco@gmail.com',
  },
  {
    image: '/images/daniel.jpg',
    name: 'Rotem Schlezinger',
    phone: '+1 (555) 345-6789',
    email: 'rotemsch22@gmail.com',
  },
];

export default function ContactPage() {
  return (
    <Container maxWidth="lg" sx={{ py: 6 }}>
      <Typography variant="h4" fontWeight={700} gutterBottom>
        Contact Us
      </Typography>
      <Typography variant="body1" color="text.secondary" mb={4}>
        Get in touch with our team. We're here to help you understand and use Elev8 to its full potential.
      </Typography>

      <Grid container spacing={6} sx={{ flexWrap: 'wrap', justifyContent: 'center'}}>
        {team.map((member, index) => (
          <Grid item xs={12} sm={6} md={6} lg={4} key={index}>
            <TeamMemberCard {...member} />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}
