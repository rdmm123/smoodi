import { Outlet, useLoaderData } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'


import Header from "components/Header";

import { ErrorLoader } from "router";
import ErrorMessage from "components/ErrorMessage";
import Footer from "./Footer";


const queryClient = new QueryClient()

export default function App() {
  const { error } = useLoaderData() as ErrorLoader;

  return (
    <>
    <QueryClientProvider client={queryClient}>
        <Header />
        <section className="grow self-center w-2/3 text-my-rose" id="content">
          {error && <ErrorMessage message={error} />}
          <Outlet />
        </section>
        <Footer />
      <ReactQueryDevtools initialIsOpen={false} buttonPosition="bottom-left" />
    </QueryClientProvider>
    </>
  )
}
