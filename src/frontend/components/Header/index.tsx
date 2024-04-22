import { Link } from "react-router-dom"
import BlendifyLogo from 'assets/blendify-logo.svg'
import { useUserContext } from "contexts/UserContext"

function Header() {
  const { user } = useUserContext();

  return (
    <section className="flex flex-row p-5 shadow-md items-center rounded-lg" id="header">
      <Link to={`/`} className="grow">
        <img src={BlendifyLogo} alt="Blendify logo" className="w-40" />
      </Link>
      {user
      ? <a
          className="py-2 px-4 text-xl hover:bg-red-100 rounded-xl text-red-500 border-2 border-red-500"
          href={BACKEND_HOST + '/auth/logout'}>
          Log Out
        </a>
      : <a
          className="mx-5 py-2 px-4 text-xl bg-blue-500 hover:bg-blue-700 rounded-xl text-white"
          href={BACKEND_HOST + '/auth/login'}>
          Log In
        </a>
      }

    </section>
  )
}

export default Header