import AddCircle from '@mui/icons-material/AddCircle';
import Error from '@mui/icons-material/Error';
import { Badge, styled, Tooltip } from '@mui/material';
import { useTranslation } from 'react-i18next';

const StyledBadge = styled(Badge)(({ size }: { size: 'small' | 'medium' }) => ({
  padding: 0,
  '& .MuiBadge-badge': {
    padding: 0,
    right: size === 'small' ? -5 : -7,
    top: size === 'small' ? 0 : 3,
  },
}));

interface BlobStateBadgeProps {
  atRisk?: boolean;
  isRookie?: boolean;
  size?: 'small' | 'medium';
  children?: React.ReactNode;
}

export const BlobStateBadge = ({ atRisk, isRookie, children, size = 'small' }: BlobStateBadgeProps) => {
  const { t } = useTranslation();

  const badgeContent = atRisk ? (
    <Tooltip title={t('states.at_risk')}>
      <Error sx={{ fontSize: size === 'small' ? 12 : 16 }} color="error" />
    </Tooltip>
  ) : isRookie ? (
    <Tooltip title={t('states.rookie')}>
      <AddCircle sx={{ fontSize: size === 'small' ? 12 : 16 }} color="success" />
    </Tooltip>
  ) : null;

  return (
    <StyledBadge size={size} badgeContent={badgeContent}>
      {children}
    </StyledBadge>
  );
};
