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
import { Add as AddIcon } from '@mui/icons-material';
import { evidenceService } from '../services/api';
import { format } from 'date-fns';

const Evidence = () => {
  const [evidence, setEvidence] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEvidence();
  }, []);

  const fetchEvidence = async () => {
    try {
      setLoading(true);
      const data = await evidenceService.getAll();
      setEvidence(data.evidence || []);
      setError(null);
    } catch (err) {
      setError('Failed to load evidence');
      console.error(err);
    } finally {
      setLoading(false);
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
        <Typography variant="h4">Evidence Collection</Typography>
        <Button variant="contained" startIcon={<AddIcon />}>
          Add Evidence
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Evidence Type</TableCell>
              <TableCell>Control ID</TableCell>
              <TableCell>Asset ID</TableCell>
              <TableCell>Collection Method</TableCell>
              <TableCell>Collected At</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {evidence.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <Typography variant="body2" color="text.secondary">
                    No evidence collected yet
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              evidence.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.evidence_type}</TableCell>
                  <TableCell>{item.control_id}</TableCell>
                  <TableCell>
                    <Typography variant="caption">{item.asset_id}</Typography>
                  </TableCell>
                  <TableCell>
                    <Chip label={item.collection_method} size="small" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    {format(new Date(item.collected_at), 'yyyy-MM-dd HH:mm')}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={item.is_valid ? 'Valid' : 'Invalid'}
                      color={item.is_valid ? 'success' : 'error'}
                      size="small"
                    />
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

export default Evidence;
