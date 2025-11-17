import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import { dashboardService } from '../services/api';
import MaturityHeatmap from '../components/MaturityHeatmap';
import StatCard from '../components/StatCard';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [heatmap, setHeatmap] = useState([]);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [summaryData, heatmapData, trendsData] = await Promise.all([
        dashboardService.getSummary(),
        dashboardService.getMaturityHeatmap(),
        dashboardService.getTrends(30),
      ]);

      setSummary(summaryData);
      setHeatmap(heatmapData.heatmap || []);
      setTrends(trendsData.trends || []);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
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

  // Prepare radar chart data for Essential Eight
  const radarData = summary?.pillars?.map(pillar => ({
    pillar: pillar.name.substring(0, 20),
    maturity: pillar.maturity_level,
    target: 3,
  })) || [];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Essential Eight Maturity Dashboard
      </Typography>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Overall Maturity Level"
            value={summary?.overall_maturity_level || 0}
            max={3}
            color="primary"
            suffix=" / 3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Average Score"
            value={summary?.average_score || 0}
            max={100}
            color="success"
            suffix="%"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Drift Events"
            value={summary?.drift_events || 0}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Open Remediation Tasks"
            value={summary?.open_remediation_tasks || 0}
            color="error"
          />
        </Grid>
      </Grid>

      {/* Maturity Heatmap */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Essential Eight Maturity Heatmap
            </Typography>
            <MaturityHeatmap data={heatmap} />
          </Paper>
        </Grid>

        {/* Radar Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Maturity Overview
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="pillar" />
                <PolarRadiusAxis angle={90} domain={[0, 3]} />
                <Radar
                  name="Current Maturity"
                  dataKey="maturity"
                  stroke="#1976d2"
                  fill="#1976d2"
                  fillOpacity={0.6}
                />
                <Radar
                  name="Target (Level 3)"
                  dataKey="target"
                  stroke="#4caf50"
                  fill="#4caf50"
                  fillOpacity={0.3}
                />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Trends Chart */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              30-Day Maturity Trend
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="average_score"
                  stroke="#1976d2"
                  name="Average Score"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Pillar Details */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Pillar Details
            </Typography>
            <Grid container spacing={2}>
              {summary?.pillars?.map((pillar, index) => (
                <Grid item xs={12} sm={6} md={3} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        {pillar.name}
                      </Typography>
                      <Typography variant="h4" component="div">
                        L{pillar.maturity_level}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {pillar.status || 'Not Assessed'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
