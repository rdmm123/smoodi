import { Link } from "react-router-dom"
import BlendifyLogo from 'assets/blendify-logo.svg'
import { useUserContext } from "contexts/UserContext"

import AnchorButton from "components/Button/AnchorButton";

function Header() {
  const { user } = useUserContext();

  return (
    <section className="flex flex-row p-5 shadow-md items-center rounded-lg" id="header">
      <Link to={`/`} className="grow">
        <img src={BlendifyLogo} alt="Blendify logo" className="w-40" />
      </Link>
      {user?.email
      ? <div className="flex items-center gap-5">
          <h1 className="text-lg">Logged in as: <span className="underline text-blue-500">{user.email}</span></h1>
          <AnchorButton href={BACKEND_HOST + "/auth/logout"} color="red" light={true}>
            Log Out
          </AnchorButton>
      </div>
      : <AnchorButton href={BACKEND_HOST + "/auth/login"} color="blue" light={false}>
          Log In
        </AnchorButton>
      }

    </section>
  )
}

export default Header