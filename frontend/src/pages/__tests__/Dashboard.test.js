import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import axios from 'axios';
import Dashboard from '../Dashboard';

// Mock axios
jest.mock('axios');

// Mock Recharts to avoid rendering issues in tests
jest.mock('recharts', () => ({
  ResponsiveContainer: ({ children }) => <div>{children}</div>,
  RadarChart: () => <div data-testid="radar-chart">Radar Chart</div>,
  PolarGrid: () => null,
  PolarAngleAxis: () => null,
  PolarRadiusAxis: () => null,
  Radar: () => null,
  LineChart: () => <div data-testid="line-chart">Line Chart</div>,
  Line: () => null,
  XAxis: () => null,
  YAxis: () => null,
  CartesianGrid: () => null,
  Tooltip: () => null,
  Legend: () => null,
}));

const mockSummaryData = {
  total_assets: 500,
  compliant_assets: 275,
  compliance_percentage: 55,
  active_drift_events: 23,
  open_remediation_tasks: 47,
  pillars: [
    {
      name: 'Application Control',
      maturity_level: 2,
      score: 67,
      status: 'on_track',
    },
    {
      name: 'Patch Applications',
      maturity_level: 1,
      score: 45,
      status: 'needs_attention',
    },
  ],
};

const mockHeatmapData = [
  {
    pillar: 'Application Control',
    level_0: 0,
    level_1: 0,
    level_2: 67,
    level_3: 0,
  },
];

const mockTrendsData = [
  {
    date: '2024-01-01',
    application_control: 2,
    patch_applications: 1,
  },
  {
    date: '2024-01-08',
    application_control: 2,
    patch_applications: 1,
  },
];

describe('Dashboard Page', () => {
  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();

    // Mock localStorage
    Storage.prototype.getItem = jest.fn(() => 'fake-token');
  });

  test('renders loading state initially', () => {
    axios.get.mockReturnValue(new Promise(() => {})); // Never resolves

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  test('renders dashboard with summary data', async () => {
    axios.get.mockImplementation((url) => {
      if (url.includes('/summary')) {
        return Promise.resolve({ data: mockSummaryData });
      }
      if (url.includes('/heatmap')) {
        return Promise.resolve({ data: mockHeatmapData });
      }
      if (url.includes('/trends')) {
        return Promise.resolve({ data: mockTrendsData });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Essential Eight Maturity Dashboard')).toBeInTheDocument();
    });

    // Check summary cards
    expect(screen.getByText('500')).toBeInTheDocument(); // Total assets
    expect(screen.getByText('275')).toBeInTheDocument(); // Compliant assets
    expect(screen.getByText('23')).toBeInTheDocument(); // Active drift
    expect(screen.getByText('47')).toBeInTheDocument(); // Open tasks
  });

  test('renders charts', async () => {
    axios.get.mockImplementation((url) => {
      if (url.includes('/summary')) {
        return Promise.resolve({ data: mockSummaryData });
      }
      if (url.includes('/heatmap')) {
        return Promise.resolve({ data: mockHeatmapData });
      }
      if (url.includes('/trends')) {
        return Promise.resolve({ data: mockTrendsData });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByTestId('radar-chart')).toBeInTheDocument();
      expect(screen.getByTestId('line-chart')).toBeInTheDocument();
    });
  });

  test('handles API error gracefully', async () => {
    axios.get.mockRejectedValue(new Error('API Error'));

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  test('displays pillar information', async () => {
    axios.get.mockImplementation((url) => {
      if (url.includes('/summary')) {
        return Promise.resolve({ data: mockSummaryData });
      }
      if (url.includes('/heatmap')) {
        return Promise.resolve({ data: mockHeatmapData });
      }
      if (url.includes('/trends')) {
        return Promise.resolve({ data: mockTrendsData });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Application Control/i)).toBeInTheDocument();
      expect(screen.getByText(/Patch Applications/i)).toBeInTheDocument();
    });
  });

  test('refreshes data on mount', async () => {
    axios.get.mockImplementation((url) => {
      if (url.includes('/summary')) {
        return Promise.resolve({ data: mockSummaryData });
      }
      if (url.includes('/heatmap')) {
        return Promise.resolve({ data: mockHeatmapData });
      }
      if (url.includes('/trends')) {
        return Promise.resolve({ data: mockTrendsData });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith(
        expect.stringContaining('/summary'),
        expect.any(Object)
      );
    });

    // Should call all three endpoints
    expect(axios.get).toHaveBeenCalledTimes(3);
  });
});
