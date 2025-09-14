import ReactDOM from 'react-dom/client';
import { RouterProvider, createRouter } from '@tanstack/react-router';
import { routeTree } from './routes/routes';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SnackbarProvider } from 'notistack';
import { SimTimeProvider } from './context/SimTimeContext';
import { AuthProvider } from './context/AuthContext';
import './i18n';
import { CurrentPageProvider } from './context/CurrentPageContext';

// Set up a Router instance
const router = createRouter({
  routeTree,
  defaultPreload: 'intent',
});

// Register things for typesafety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

const queryClient = new QueryClient();

const rootElement = document.getElementById('app')!;

if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <QueryClientProvider client={queryClient}>
      <SnackbarProvider>
        <AuthProvider>
          <SimTimeProvider>
            <CurrentPageProvider>
              <RouterProvider router={router} />
            </CurrentPageProvider>
          </SimTimeProvider>
        </AuthProvider>
      </SnackbarProvider>
    </QueryClientProvider>,
  );
}
