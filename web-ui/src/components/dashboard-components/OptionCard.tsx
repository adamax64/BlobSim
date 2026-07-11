import { Box, Card, CardActionArea, Typography } from '@mui/material';

type OptionCardProps = {
  title: string;
  icon: React.ElementType;
  onClick: () => void;
};

const OptionCard = ({ title, icon: Icon, onClick }: OptionCardProps) => {
  return (
    <Card>
      <CardActionArea
        onClick={onClick}
        sx={{
          '&:hover': {
            backgroundColor: 'action.selectedHover',
          },
          height: '100%',
          padding: 3,
        }}
      >
        <Box display="flex" alignItems="center" gap={1} height="100%">
          <Icon fontSize="large" />
          <Typography variant="h4">{title}</Typography>
        </Box>
      </CardActionArea>
    </Card>
  );
};

export default OptionCard;
