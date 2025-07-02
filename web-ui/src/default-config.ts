import { Configuration } from '../generated';

console.log('Default configuration loaded with base path:', import.meta.env.VITE_API_BASE_URL);

const defaultConfig = new Configuration({
  basePath: import.meta.env.VITE_API_BASE_URL,
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
