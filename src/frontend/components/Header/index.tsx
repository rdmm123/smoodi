import { Link } from "react-router-dom"

const Header = () => (
    <section className="flex flex-row p-5 shadow-md items-center rounded-lg" id="header">
      <Link to={`/`} className="grow text-4xl font-bold">Blendify</Link>
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
)

export default Header