import { Outlet, useLoaderData, useLocation } from "react-router-dom";

import Header from "components/Header";
import { UserContextProvider } from "contexts/UserContext";
import { ErrorLoader } from "router";
import ErrorMessage from "components/ErrorMessage";

export default function App() {
  const { error } = useLoaderData() as ErrorLoader;
  const location = useLocation();

  const isHomePage = location.pathname == '/';
  return (
    <>
    <UserContextProvider>
      {!isHomePage && <Header />}
    
      <section className="h-full w-full text-my-rose flex items-center justify-center" id="content">
        {error && <ErrorMessage message={error} />}
        <Outlet />
      </section>
    </UserContextProvider>
    </>
  )
}
