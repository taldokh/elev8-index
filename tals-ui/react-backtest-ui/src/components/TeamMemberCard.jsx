// src/components/TeamMemberCard.jsx
import React from 'react';
import { Card, CardContent, Avatar, Typography, Box } from '@mui/material';

export default function TeamMemberCard({ image, name, phone, email }) {
  return (
    <Card sx={{
        display: 'flex',
        alignItems: 'center',
        p: 3,
        borderRadius: 3,
        boxShadow: 2,
        width: '100%',
        minHeight: 130,
        minWidth: 400
      }}>
      <Avatar
        src={image}
        alt={name}
        sx={{ width: 72, height: 72, mr: 3 }}
      />
      <CardContent sx={{ p: 0 }}>
        <Typography variant="h6" fontWeight={600}>{name}</Typography>
        <Typography variant="body2" color="text.secondary">{phone}</Typography>
        <Typography variant="body2" color="text.secondary">{email}</Typography>
      </CardContent>
    </Card>
  );
}
