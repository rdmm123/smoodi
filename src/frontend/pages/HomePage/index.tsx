import { Logo, LogoSize } from "components/Logo";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Link } from "react-router-dom";

import { useCurrentUserQuery } from "hooks/user";

function HomePage() {
  const { data: user } = useCurrentUserQuery();
  const userLoggedIn = !!user?.email;

  return <div className="flex flex-col justify-center items-center gap-16 h-full">
    <Logo size={LogoSize.X_X_LARGE} style="vertical" />

    <p className="text-white text-center text-xl">Combine your and your friends' favorite Spotify songs into one awesome playlist (or smoodi).
      Connect your accounts, merge your top tracks, and enjoy a shared music experience.
      Perfect for parties or hangouts!</p>

    <Card className="shadow-[0_0_10px_3px] shadow-my-rose/50 rounded-3xl">
      <CardContent className="pt-6 flex items-center gap-4">
        <p className="text-2xl">Get started:</p>
        <Button className="text-xl py-7 rounded-xl" asChild>
          {userLoggedIn
          ? <Link to={"/session"}>Create Session</Link>
          : <a href={BACKEND_HOST + "/auth/login"}>Log In with Spotify</a>}
        </Button>
      </CardContent>
    </Card>
  </div>
}

export default HomePage;