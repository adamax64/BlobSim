import { Box, Card, CardActionArea, Typography } from '@mui/material';
import { useIsTablet } from '../../hooks/useIsTablet';

type OptionCardProps = {
  title: string;
  icon: React.ElementType;
  onClick: () => void;
  badge?: React.ReactNode;
};

const OptionCard = ({ title, icon: Icon, onClick, badge }: OptionCardProps) => {
  const isTable = useIsTablet();

  return (
    <Card sx={{ height: '100%', position: 'relative' }}>
      <CardActionArea
        onClick={onClick}
        sx={{
          '&:hover': {
            backgroundColor: 'action.selectedHover',
          },
          height: '100%',
          padding: isTable ? 3 : 6,
        }}
      >
        <Box display="flex" justifyContent="space-between" gap={1.5} height="100%">
          <Box display="flex" alignItems="center" gap={1.5}>
            <Icon fontSize="large" />
            <Typography variant="h4">{title}</Typography>
          </Box>
          {badge}
        </Box>
      </CardActionArea>
    </Card>
  );
};

export default OptionCard;
