import { Configuration } from '../generated';

const defaultConfig = new Configuration({
  basePath: 'http://localhost:8000',
  middleware: [
    {
      pre: async (context) => {
        const token = localStorage.getItem('adminToken');
        if (token) {
          context.init.headers = {
            ...context.init.headers,
            Authorization: `Bearer ${token}`,
          };
        }
        return context;
      },
    },
  ],
});

export default defaultConfig;
