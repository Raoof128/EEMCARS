import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import { PlayArrow as PlayIcon } from '@mui/icons-material';
import { assessmentService } from '../services/api';
import { format } from 'date-fns';

const Assessments = () => {
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAssessments();
  }, []);

  const fetchAssessments = async () => {
    try {
      setLoading(true);
      const data = await assessmentService.getAll();
      setAssessments(data.runs || []);
      setError(null);
    } catch (err) {
      setError('Failed to load assessments');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerAssessment = async () => {
    try {
      await assessmentService.triggerAssessment({
        run_type: 'OnDemand',
        asset_ids: [],
        control_ids: [],
      });
      fetchAssessments();
    } catch (err) {
      console.error('Failed to trigger assessment', err);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Completed':
        return 'success';
      case 'Running':
        return 'info';
      case 'Failed':
        return 'error';
      default:
        return 'default';
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
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Assessment Runs</Typography>
        <Button variant="contained" startIcon={<PlayIcon />} onClick={handleTriggerAssessment}>
          Run Assessment
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Run Type</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Started At</TableCell>
              <TableCell>Completed At</TableCell>
              <TableCell>Assets</TableCell>
              <TableCell>Controls</TableCell>
              <TableCell>Maturity Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {assessments.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  <Typography variant="body2" color="text.secondary">
                    No assessment runs yet
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              assessments.map((assessment) => (
                <TableRow key={assessment.id}>
                  <TableCell>{assessment.run_type}</TableCell>
                  <TableCell>
                    <Chip label={assessment.status} color={getStatusColor(assessment.status)} size="small" />
                  </TableCell>
                  <TableCell>{format(new Date(assessment.started_at), 'yyyy-MM-dd HH:mm')}</TableCell>
                  <TableCell>
                    {assessment.completed_at
                      ? format(new Date(assessment.completed_at), 'yyyy-MM-dd HH:mm')
                      : '-'}
                  </TableCell>
                  <TableCell>{assessment.total_assets || 0}</TableCell>
                  <TableCell>{assessment.total_controls || 0}</TableCell>
                  <TableCell>
                    {assessment.overall_maturity_score
                      ? assessment.overall_maturity_score.toFixed(2)
                      : '-'}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default Assessments;
