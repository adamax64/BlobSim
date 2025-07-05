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
      onError: async (context) => {
        const error = context.error as { message?: string };
        const errorMessage = error?.message || 'An unknown error occurred.';
        throw errorMessage;
      },
    },
  ],
});

export default defaultConfig;
