import { Box, Button } from '@mui/material';
import { HU, GB } from 'country-flag-icons/react/3x2';
import { useTranslation } from 'react-i18next';

const languages = [
  { code: 'en', title: 'English', Flag: GB },
  { code: 'hu', title: 'Magyar', Flag: HU },
];

export function LanguageSwitcher() {
  const { i18n } = useTranslation();

  const handleLanguageChange = (lang: string) => {
    i18n.changeLanguage(lang);
  };

  return (
    <Box margin={1} gap={1} display="flex">
      {languages.map(({ code, title, Flag }) => (
        <Button
          key={code}
          color={i18n.language.startsWith(code) ? 'primary' : 'inherit'}
          variant="contained"
          sx={{ padding: '4px', minWidth: 0 }}
          onClick={() => handleLanguageChange(code)}
        >
          <Flag title={title} style={{ width: '2em', height: 'auto', display: 'block' }} />
        </Button>
      ))}
    </Box>
  );
}
