import { Outlet, useLoaderData } from "react-router-dom";

import Header from "components/Header";
import { UserContextProvider } from "contexts/UserContext";
import { ErrorLoader } from "router";

export default function App() {
  const { error } = useLoaderData() as ErrorLoader;

  return (
    <>
    <UserContextProvider>
      <Header />
    
      <section className="p-10 flex flex-col justify-center items-center w-100" id="content">

        {error &&
          <div className="bg-red-200 outline outline-1 outline-red-500 text-red-500 rounded-xl p-3 text-center mb-5">
            <p className="text-lg">{error}</p>
          </div>}
          
          <Outlet />
      </section>
    </UserContextProvider>
    </>
  )
}
