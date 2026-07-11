import { Box, Card, CardActionArea, Typography } from '@mui/material';
import { useIsTablet } from '../../hooks/useIsTablet';

type OptionCardProps = {
  title: string;
  icon: React.ElementType;
  onClick: () => void;
};

const OptionCard = ({ title, icon: Icon, onClick }: OptionCardProps) => {
  const isTable = useIsTablet();

  return (
    <Card sx={{ height: '100%' }}>
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
        <Box display="flex" alignItems="center" gap={1.5} height="100%">
          <Icon fontSize="large" />
          <Typography variant="h4">{title}</Typography>
        </Box>
      </CardActionArea>
    </Card>
  );
};

export default OptionCard;
