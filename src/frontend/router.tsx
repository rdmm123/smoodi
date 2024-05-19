import { createBrowserRouter, RouteObject } from 'react-router-dom';
import App from 'components/App';
import ErrorPage from 'pages/ErrorPage';
import HomePage from 'pages/HomePage';
import SessionPage from "pages/SessionPage";
import BlendifyPage from 'pages/BlendifyPage';
import AfterLoginPage from 'pages/AfterLoginPage';
import PrivatePage from 'pages/PrivatePage';

export interface ErrorLoader {
  error: string
}

const routes: RouteObject[] = [
  {
    path: "/",
    element: <App />,

    loader: ({ request }) => {

      const url = new URL(request.url);
      const error  = url.searchParams.get("error");
      return { error } as ErrorLoader;
    },
    
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/session",
        element: <PrivatePage><SessionPage /></PrivatePage>,
      },
      {
        path: "/blendify",
        element: <PrivatePage><BlendifyPage /></PrivatePage>,
      }
    ],
  },
  {
    path: "/after_login",
    element: <AfterLoginPage />
  }
];

const router = createBrowserRouter(routes);

export default router;