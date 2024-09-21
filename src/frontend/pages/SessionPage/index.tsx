import CopyInput from "components/CopyInput";
import CurrentSession from "components/CurrentSession";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

import { useCurrentUserQuery, useUserSessionQuery } from "hooks/user";

export default function SessionPage() {
  const { data: user } = useCurrentUserQuery();
  const { data: session } = useUserSessionQuery(user);

  const allowStart = session && session.length > 0;

  return <div className="flex flex-col items-center justify-center h-full gap-5">
    <h1 className="text-5xl font-bold text-center font-serif">Your Session</h1>
    <div className="w-full">
      <p className="text-xl text-center text-slate-50 mb-3">Share this url with your friends for them to join!</p>
      <CopyInput text={`${BACKEND_HOST}/auth/login/${user?.id}`} />
    </div>
    <CurrentSession />
    <Button variant={allowStart ? "default" : "disabled"} className="rounded-xl" asChild>
      <Link to={allowStart ? "/blendify" : "#"} className="text-xl">Let's Go!</Link>
    </Button>
  </div>;
}
