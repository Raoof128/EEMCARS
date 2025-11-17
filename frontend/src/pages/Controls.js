import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import { ExpandMore as ExpandMoreIcon } from '@mui/icons-material';
import { controlsService } from '../services/api';

const Controls = () => {
  const [controls, setControls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedControl, setSelectedControl] = useState(null);

  useEffect(() => {
    fetchControls();
  }, []);

  const fetchControls = async () => {
    try {
      setLoading(true);
      const data = await controlsService.getAll();
      setControls(data.controls || []);
      setError(null);
    } catch (err) {
      setError('Failed to load controls');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleControlClick = async (controlId) => {
    try {
      const data = await controlsService.getById(controlId);
      setSelectedControl(data);
    } catch (err) {
      console.error('Failed to load control details', err);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Essential Eight Controls
      </Typography>

      <Grid container spacing={3}>
        {controls.map((control) => (
          <Grid item xs={12} md={6} key={control.id}>
            <Accordion onChange={() => handleControlClick(control.control_id)}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                  <Chip label={control.control_id} color="primary" />
                  <Typography variant="subtitle1">{control.name}</Typography>
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {control.description}
                </Typography>
                <Typography variant="caption" display="block" gutterBottom>
                  Pillar: <strong>{control.pillar}</strong>
                </Typography>
                <Typography variant="caption" display="block">
                  ACSC Reference: <strong>{control.acsc_reference}</strong>
                </Typography>

                {selectedControl && selectedControl.control_id === control.control_id && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Maturity Requirements:
                    </Typography>
                    {selectedControl.requirements?.map((req) => (
                      <Box key={req.maturity_level} sx={{ mb: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                        <Chip label={`Level ${req.maturity_level}`} size="small" sx={{ mb: 1 }} />
                        <Typography variant="body2">{req.requirement_text}</Typography>
                      </Box>
                    ))}
                  </Box>
                )}
              </AccordionDetails>
            </Accordion>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Controls;
