import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

import Dashboard from './pages/Dashboard';
import Controls from './pages/Controls';
import Evidence from './pages/Evidence';
import Assessments from './pages/Assessments';
import Remediation from './pages/Remediation';
import Reports from './pages/Reports';
import Login from './pages/Login';
import Sidebar from './components/Sidebar';
import Header from './components/Header';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = React.useState(
    localStorage.getItem('token') !== null
  );

  const handleLogin = (token) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Login onLogin={handleLogin} />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex' }}>
          <Sidebar onLogout={handleLogout} />
          <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
            <Header />
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/controls" element={<Controls />} />
              <Route path="/evidence" element={<Evidence />} />
              <Route path="/assessments" element={<Assessments />} />
              <Route path="/remediation" element={<Remediation />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
