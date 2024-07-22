import { Link } from "react-router-dom"
import { useUserContext } from "contexts/UserContext"

import AnchorButton from "components/Button/AnchorButton";
import { LogoSize, Logo } from "components/Logo";

function Header() {
  const { user } = useUserContext();

  return (
    <header className="flex flex-row p-5 drop-shadow-xl items-center justify-between rounded-lg bg-my-purple-950">
      <Link to={`/`}>
        <Logo size={LogoSize.LARGE} />
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

    </header>
  )
}

export default Header