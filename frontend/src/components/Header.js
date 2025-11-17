import React from 'react';
import { AppBar, Toolbar, Typography, Box, Chip } from '@mui/material';

const Header = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{"username":"admin","role":"Admin"}');

  return (
    <AppBar
      position="fixed"
      sx={{
        width: `calc(100% - 260px)`,
        ml: `260px`,
        backgroundColor: 'background.paper',
        color: 'text.primary',
        boxShadow: 1,
      }}
    >
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Essential Eight Maturity Assessment
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Chip label={user.role} color="primary" size="small" />
          <Typography variant="body2">{user.username}</Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
