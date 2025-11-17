import React from 'react';
import { Card, CardContent, Typography, Box, LinearProgress } from '@mui/material';

const StatCard = ({ title, value, max, color = 'primary', suffix = '' }) => {
  const percentage = max ? (value / max) * 100 : 0;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography color="text.secondary" gutterBottom variant="overline">
          {title}
        </Typography>
        <Typography variant="h3" component="div" color={`${color}.main`}>
          {value}{suffix}
        </Typography>
        {max && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress
              variant="determinate"
              value={percentage}
              color={color}
              sx={{ height: 8, borderRadius: 4 }}
            />
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default StatCard;
