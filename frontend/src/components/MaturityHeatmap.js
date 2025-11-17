import React from 'react';
import { Box, Typography, Chip } from '@mui/material';

const MaturityHeatmap = ({ data }) => {
  const getMaturityColor = (level) => {
    switch (level) {
      case 3:
        return '#4caf50'; // Green
      case 2:
        return '#ff9800'; // Orange
      case 1:
        return '#f44336'; // Red
      default:
        return '#9e9e9e'; // Grey
    }
  };

  const getMaturityLabel = (level) => {
    return `Level ${level}`;
  };

  return (
    <Box sx={{ overflowX: 'auto' }}>
      {data.map((control, index) => (
        <Box
          key={index}
          sx={{
            display: 'flex',
            alignItems: 'center',
            p: 1.5,
            mb: 1,
            borderRadius: 1,
            backgroundColor: 'background.paper',
            border: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Box sx={{ flex: 1, mr: 2 }}>
            <Typography variant="subtitle2" fontWeight="bold">
              {control.control_id}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {control.control_name}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {control.pillar}
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Chip
              label={getMaturityLabel(control.maturity_level)}
              sx={{
                backgroundColor: getMaturityColor(control.maturity_level),
                color: 'white',
                fontWeight: 'bold',
              }}
            />
            <Typography variant="body2" sx={{ minWidth: 60 }}>
              Score: {control.score}%
            </Typography>
          </Box>
        </Box>
      ))}
    </Box>
  );
};

export default MaturityHeatmap;
