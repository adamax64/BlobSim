import { Paper } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { PageFrame } from '../common/PageFrame';
import { markdownComponents } from '../wiki-components/markdownComponents';
import championshipMd from '../../wiki/en/championship.md?raw';

export const WikiPage = () => {
  return (
    <PageFrame pageName="wiki">
      <Paper sx={{ p: { xs: 2, sm: 4 }, maxWidth: 900, width: '100%', mx: 'auto' }}>
        <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdownComponents}>
          {championshipMd}
        </ReactMarkdown>
      </Paper>
    </PageFrame>
  );
};
