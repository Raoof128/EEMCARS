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
  IconButton,
} from '@mui/material';
import { PlayArrow as PlayIcon, Add as AddIcon } from '@mui/icons-material';
import { remediationService } from '../services/api';
import { format } from 'date-fns';

const Remediation = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await remediationService.getTasks();
      setTasks(data.tasks || []);
      setError(null);
    } catch (err) {
      setError('Failed to load remediation tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteTask = async (taskId) => {
    try {
      await remediationService.executeTask(taskId);
      fetchTasks();
    } catch (err) {
      console.error('Failed to execute task', err);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Critical':
        return 'error';
      case 'High':
        return 'warning';
      case 'Medium':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Completed':
        return 'success';
      case 'InProgress':
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
        <Typography variant="h4">Remediation Tasks</Typography>
        <Button variant="contained" startIcon={<AddIcon />}>
          Create Task
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Task Type</TableCell>
              <TableCell>Priority</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created At</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <Typography variant="body2" color="text.secondary">
                    No remediation tasks
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              tasks.map((task) => (
                <TableRow key={task.id}>
                  <TableCell>
                    <Typography variant="body2">{task.title}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {task.description}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip label={task.task_type} size="small" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    <Chip label={task.priority} color={getPriorityColor(task.priority)} size="small" />
                  </TableCell>
                  <TableCell>
                    <Chip label={task.status} color={getStatusColor(task.status)} size="small" />
                  </TableCell>
                  <TableCell>{format(new Date(task.created_at), 'yyyy-MM-dd HH:mm')}</TableCell>
                  <TableCell>
                    {task.status === 'Open' && (
                      <IconButton
                        size="small"
                        color="primary"
                        onClick={() => handleExecuteTask(task.id)}
                      >
                        <PlayIcon />
                      </IconButton>
                    )}
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

export default Remediation;
