import { createBrowserRouter, RouteObject } from 'react-router-dom';
import App from 'components/App';
import ErrorPage from 'pages/ErrorPage';
import HomePage from 'pages/HomePage';
import BlenderPage from 'pages/BlenderPage';

const routes: RouteObject[] = [
  {
    path: "/",
    element: <App />,

    loader: ({ request }) => {
      const url = new URL(request.url);
      const error  = url.searchParams.get("error");

      return { error };
    },
    
    // errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/blender",
        element: <BlenderPage />,
      }
    ]
  }
];

const router = createBrowserRouter(routes);

export default router;