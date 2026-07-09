import { Box, Grid, useMediaQuery, useTheme } from '@mui/material';
import { StandingsSnippetDto } from '../../../../../generated';
import { getShortName } from '../../../../utils/blob-name-utils';
import { BlobIcon } from '../../../icons/BlobIcon';
import DynamicTooltip from '../../DynamicTooltip';
import { useCallback } from 'react';

const StandingSnippetWidget = ({ standingsData }: { standingsData: StandingsSnippetDto[] }) => {
  const onlyIcon = useMediaQuery('(max-width:425px)');

  const blobName = useCallback((standing: StandingsSnippetDto) => {
    if (onlyIcon) {
      return (
        <DynamicTooltip title={standing.blobName}>
          <Box display="flex" width="100%" height="100%" justifyContent="center" alignItems="center">
            <BlobIcon size={16} color={standing.blobColor} />
          </Box>
        </DynamicTooltip>
      );
    }

    return (
      <Box
        display="flex"
        width="100%"
        alignItems="center"
        gap={0.5}
        textOverflow="ellipsis"
        overflow="hidden"
        whiteSpace="nowrap"
      >
        <Box>
          <BlobIcon size={16} color={standing.blobColor} />
        </Box>
        {getShortName(standing.blobName)}
      </Box>
    );
  }, []);

  return (
    <Grid
      container
      width="100%"
      border={1}
      borderColor="divider"
      borderRadius={1}
      bgcolor="background.default"
      columns={3}
    >
      {standingsData.map((standing, index) => (
        <Grid
          key={index}
          container
          width="100%"
          borderBottom={index < standingsData.length - 1 ? 1 : 0}
          borderColor="divider"
        >
          <Grid paddingX={0.5}>{standing.position}</Grid>
          <Grid size="grow" paddingX={0.5} borderLeft={1} borderRight={1} borderColor="divider">
            {blobName(standing)}
          </Grid>
          <Grid paddingX={0.5}>{standing.points}</Grid>
        </Grid>
      ))}
    </Grid>
  );
};

export default StandingSnippetWidget;
