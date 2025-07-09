import { Box, Button, Card, CardContent, TextField, Typography } from '@mui/material';
import { useMutation } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { useAuth } from '../../context/AuthContext';
import { AuthApi } from '../../../generated';
import defaultConfig from '../../default-config';
import { LoadingOverlay } from '../common/LoadingOverlay';
import { useSnackbar } from 'notistack';
import { useTranslation } from 'react-i18next';
import { PageFrame } from '../common/PageFrame';

export const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const { t } = useTranslation();

  const authApi = new AuthApi(defaultConfig);
  const { mutate: loginMutation, isPending } = useMutation({
    mutationFn: () => authApi.loginAuthLoginPost({ loginRequest: { username, password } }),
    onSuccess: (data) => {
      login(data.token);
      navigate({ to: '/dashboard' });
    },
    onError: () => {
      enqueueSnackbar(t('login.invalid_credentials'), { variant: 'error' });
    },
  });

  useEffect(() => {
    if (isAuthenticated) {
      navigate({ to: '/dashboard' });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loginMutation();
  };

  return (
    <PageFrame showLoading={isPending}>
      <Box display="flex" justifyContent="center" alignItems="center" flexGrow={1}>
        <Card sx={{ width: '100%', maxWidth: 400 }}>
          <CardContent>
            <Typography variant="h5" component="h1" gutterBottom textAlign="center">
              {t('login.title')}
            </Typography>
            <form onSubmit={handleSubmit}>
              <Box display="flex" flexDirection="column" gap={2}>
                <TextField
                  label={t('login.username')}
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  fullWidth
                />
                <TextField
                  label={t('login.password')}
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  fullWidth
                />
                <Button type="submit" variant="contained" color="primary" fullWidth>
                  {t('login.login_button')}
                </Button>
              </Box>
            </form>
          </CardContent>
        </Card>
      </Box>
    </PageFrame>
  );
};
