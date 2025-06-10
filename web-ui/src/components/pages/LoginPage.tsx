import { Box, Button, Card, CardContent, TextField, Typography } from '@mui/material';
import { useMutation } from '@tanstack/react-query';
import { useState } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { useAuth } from '../../context/AuthContext';
import { AuthApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { LoadingOverlay } from '../common/LoadingOverlay';
import { useSnackbar } from 'notistack';

export const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();

  const authApi = new AuthApi(defaultConfig);
  const { mutate: loginMutation, isPending } = useMutation({
    mutationFn: () => authApi.loginAuthLoginPost({ loginRequest: { username, password } }),
    onSuccess: (data) => {
      login(data.token);
      navigate({ to: '/dashboard' });
    },
    onError: () => {
      enqueueSnackbar('Invalid credentials', { variant: 'error' });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loginMutation();
  };

  return (
    <Box
      sx={{
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f5f5f5',
      }}
    >
      <Card sx={{ width: '100%', maxWidth: 400 }}>
        <CardContent>
          <Typography variant="h5" component="h1" gutterBottom textAlign="center">
            Admin Login
          </Typography>
          <form onSubmit={handleSubmit}>
            <Box display="flex" flexDirection="column" gap={2}>
              <TextField
                label="Username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                fullWidth
              />
              <TextField
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                fullWidth
              />
              <Button type="submit" variant="contained" color="primary" fullWidth>
                Login
              </Button>
            </Box>
          </form>
        </CardContent>
      </Card>
      {isPending && <LoadingOverlay />}
    </Box>
  );
};
