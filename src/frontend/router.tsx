import { createBrowserRouter, RouteObject } from 'react-router-dom';
import App from 'components/App';
import ErrorPage from 'error-page';
import Home from 'components/Home'
import Blender from 'components/Blender';

const routes: RouteObject[] = [
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/blender",
        element: <Blender />,
      },
    ]
  },
];

const router = createBrowserRouter(routes);

export default router;