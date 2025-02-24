import { createRootRoute, createRoute, redirect } from '@tanstack/react-router'
import { DashboardPage } from '../components/DashboardPage'
import { BlobsPage } from '../components/BlobsPage'
import { StandingsPage } from '../components/StandingsPage'
import { RootLayout } from '../components/RootLayout'
import { CalendarPage } from '../components/CalendarPage'

const RootRoute = createRootRoute({
  component: RootLayout,
})

export const routeTree = RootRoute.addChildren([
  createRoute({
    path: '/',
    loader: () => redirect({ to: '/dashboard' }),
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
    path: '/standings',
    component: StandingsPage,
    getParentRoute: () => RootRoute,
  }),
  createRoute({
    path: '/calendar',
    component: CalendarPage,
    getParentRoute: () => RootRoute,
  }),
]);
