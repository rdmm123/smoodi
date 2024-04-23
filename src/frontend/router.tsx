import { createBrowserRouter, redirect, RouteObject } from 'react-router-dom';
import App from 'components/App';
import ErrorPage from 'pages/ErrorPage';
import HomePage from 'pages/HomePage';
import SessionPage from "pages/SessionPage";
import BlendifyPage from 'pages/BlendifyPage';
import { fetchCurrentUser } from 'services/api';

const userLoader = async () => {
  // TODO: check if this generates a duplicate call with the context
  const user = await fetchCurrentUser();

  if (!user) {
    return redirect('/')
  }

  return null;
}

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
        path: "/session",
        element: <SessionPage />,
        loader: userLoader
      },
      {
        path: "/blendify",
        element: <BlendifyPage />,
        loader: userLoader
      }
    ]
  }
];

const router = createBrowserRouter(routes);

export default router;