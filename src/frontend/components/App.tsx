import { Outlet, Link } from "react-router-dom";

export default function App() {
  return (
    <>
    <section className="flex flex-row p-5 bg-slate-100 items-center" id="header">
      <Link to={`/`} className="grow text-4xl font-bold">Blendify</Link>
      {/* TODO: Create button component */}
      {/* <LinkButton text='Log In' href={BACKEND_HOST + '/auth/login'} color="blue" className="mx-5"/>
      <LinkButton text='Log Out' href={BACKEND_HOST + '/auth/logout'} color="red" light={true}/> */}
      <a
        className="mx-5 py-2 px-4 text-xl bg-blue-500 hover:bg-blue-700 rounded-xl text-white"
        href={BACKEND_HOST + '/auth/login'}>
          Log In
      </a>
      <a
        className="py-2 px-4 text-xl hover:bg-red-100 rounded-xl text-red-500 border-2 border-red-500"
        href={BACKEND_HOST + '/auth/logout'}>
          Log Out
      </a>
    </section>
    <section className="p-10 flex justify-center items-center" id="content">
      <Outlet />
    </section>
    </>
  )
}
