import { IconButton, Tooltip } from '@mui/material';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import { useTheme } from '@mui/material/styles';
import { useThemeMode } from '../../context/ThemeModeContext';
import { useTranslation } from 'react-i18next';

export const ThemeModeSwitcher: React.FC = () => {
  const theme = useTheme();
  const { mode, toggleMode } = useThemeMode();
  const { t } = useTranslation();

  return (
    <Tooltip title={mode === 'dark' ? t('theme.switch_to_light') : t('theme.switch_to_dark')}>
      <IconButton color="inherit" onClick={toggleMode} size="large">
        {theme.palette.mode === 'dark' ? <LightModeIcon /> : <DarkModeIcon />}
      </IconButton>
    </Tooltip>
  );
};

export default ThemeModeSwitcher;
