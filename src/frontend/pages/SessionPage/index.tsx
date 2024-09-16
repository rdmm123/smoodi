import CopyInput from "components/CopyInput";
import CurrentSession from "components/CurrentSession";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

import { useCurrentUserQuery } from "hooks/user";

export default function SessionPage() {
  const { data: user } = useCurrentUserQuery();

  return <div className="flex flex-col items-center justify-center h-full gap-5">
    <h1 className="text-5xl font-bold text-center font-serif">Your Session</h1>
    <div className="w-full">
      <p className="text-xl text-center text-slate-50 mb-3">Share this url with your friends for them to join!</p>
      <CopyInput text={`${BACKEND_HOST}/auth/login/${user?.id}`} />
    </div>
    <CurrentSession />
    <Button className="rounded-xl" asChild>
      {/* TODO: Block this button until there is at least 1 member in the session */}
      <Link to={"/blendify"} className="text-xl">Let's Go!</Link>
    </Button>
  </div>;
}
