import React from 'react';
import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button";

import { useCurrentUserQuery } from 'hooks/user';
import { LogoSize, Logo } from "components/Logo";
import UserDropdown from './UserDropdown';


const LoginButton: React.FC = () => (
  <Button asChild>
    <a href={BACKEND_HOST + "/auth/login"}>Log In</a>
  </Button>
)

function Header(): React.ReactElement {
  const { data: user } = useCurrentUserQuery()

  return (
    <header className="flex flex-row p-4 drop-shadow-xl items-center justify-between rounded-lg bg-my-purple-950">
      <Link to={`/`}>
        <Logo size={LogoSize.LARGE} />
      </Link>
      {user?.email
      ?
        <UserDropdown />
      : <LoginButton />}
    </header>
  )
}

export default Header