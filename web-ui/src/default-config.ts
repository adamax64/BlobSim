import { Configuration } from '../generated';

// Add type for window.env
declare global {
  interface Window {
    env?: { [key: string]: string };
  }
}

const defaultConfig = new Configuration({
  basePath: (window.env && window.env.VITE_API_BASE_URL) || import.meta.env.VITE_API_BASE_URL,
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
