import { createRootRoute, createRoute, redirect } from '@tanstack/react-router';
import { DashboardPage } from '../components/pages/DashboardPage';
import { BlobsPage } from '../components/pages/BlobsPage';
import { StandingsPage } from '../components/pages/StandingsPage';
import { RootLayout } from '../components/RootLayout';
import { CalendarPage } from '../components/pages/CalendarPage';
import { FactoryPage } from '../components/pages/FactoryPage';
import { EventPage } from '../components/pages/EventPage';
import { LoginPage } from '../components/pages/LoginPage';

const RootRoute = createRootRoute({
  component: RootLayout,
});

export const routeTree = RootRoute.addChildren([
  createRoute({
    path: '/',
    loader: () => redirect({ to: '/dashboard' }),
    getParentRoute: () => RootRoute,
  }),
  createRoute({
    path: '/login',
    component: LoginPage,
    getParentRoute: () => RootRoute,
  }),
  createRoute({
    path: '/dashboard',
    component: DashboardPage,
    getParentRoute: () => RootRoute,
  }),
  createRoute({
    path: '/blobs',
    component: BlobsPage,
    getParentRoute: () => RootRoute,
  }),
  createRoute({
    path: '/factory',
    component: FactoryPage,
    getParentRoute: () => RootRoute,
  }),
  createRoute({
    path: '/standings',
    component: StandingsPage,
    getParentRoute: () => RootRoute,
  }),
  createRoute({
    path: '/calendar',
    component: CalendarPage,
    getParentRoute: () => RootRoute,
  }),
  createRoute({
    path: '/event',
    component: EventPage,
    getParentRoute: () => RootRoute,
  }),
]);
