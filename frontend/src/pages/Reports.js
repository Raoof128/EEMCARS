import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from '@mui/material';
import { Download as DownloadIcon } from '@mui/icons-material';
import { reportsService } from '../services/api';

const Reports = () => {
  const [reportType, setReportType] = useState('EXECUTIVE');
  const [format, setFormat] = useState('PDF');
  const [generating, setGenerating] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerateReport = async () => {
    try {
      setGenerating(true);
      setError(null);
      setSuccess(false);

      const result = await reportsService.generate({
        report_type: reportType,
        format: format,
        parameters: {},
      });

      setSuccess(true);
      console.log('Report generated:', result);
    } catch (err) {
      setError('Failed to generate report');
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Reports
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Generate Report
            </Typography>

            {success && (
              <Alert severity="success" sx={{ mb: 2 }}>
                Report generated successfully!
              </Alert>
            )}

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Report Type</InputLabel>
              <Select value={reportType} onChange={(e) => setReportType(e.target.value)} label="Report Type">
                <MenuItem value="EXECUTIVE">Executive Summary</MenuItem>
                <MenuItem value="DETAILED">Detailed Technical Report</MenuItem>
                <MenuItem value="COMPLIANCE">Compliance Report</MenuItem>
                <MenuItem value="TREND">Trend Analysis</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Format</InputLabel>
              <Select value={format} onChange={(e) => setFormat(e.target.value)} label="Format">
                <MenuItem value="PDF">PDF</MenuItem>
                <MenuItem value="CSV">CSV</MenuItem>
                <MenuItem value="JSON">JSON</MenuItem>
                <MenuItem value="HTML">HTML</MenuItem>
              </Select>
            </FormControl>

            <Button
              fullWidth
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={handleGenerateReport}
              disabled={generating}
            >
              {generating ? 'Generating...' : 'Generate Report'}
            </Button>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Report Templates
              </Typography>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2">Executive Summary</Typography>
                <Typography variant="body2" color="text.secondary">
                  High-level overview of Essential Eight maturity aligned with ACSC guidance
                </Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2">Detailed Technical Report</Typography>
                <Typography variant="body2" color="text.secondary">
                  Comprehensive technical assessment with evidence and findings
                </Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2">Compliance Report</Typography>
                <Typography variant="body2" color="text.secondary">
                  Compliance checklist and gap analysis for audit purposes
                </Typography>
              </Box>

              <Box>
                <Typography variant="subtitle2">Trend Analysis</Typography>
                <Typography variant="body2" color="text.secondary">
                  Historical trends and maturity progression over time
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Reports;
