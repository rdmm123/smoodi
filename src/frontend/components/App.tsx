import { Outlet, useLoaderData } from "react-router-dom";

import Header from "components/Header";
import { UserContextProvider } from "contexts/UserContext";
import { ErrorLoader } from "router";
import ErrorMessage from "components/ErrorMessage";

export default function App() {
  const { error } = useLoaderData() as ErrorLoader;

  return (
    <>
    <UserContextProvider>
      <Header />
      <section className="grow self-center w-2/3 text-my-rose" id="content">
        {error && <ErrorMessage message={error} />}
        <Outlet />
      </section>
    </UserContextProvider>
    </>
  )
}
