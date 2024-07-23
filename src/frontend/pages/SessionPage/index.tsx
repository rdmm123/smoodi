import { useUserContext } from "contexts/UserContext";
import { useEffect } from "react";
import CopyInput from "components/CopyInput";
import LinkButton from "components/Button/LinkButton";
import CurrentSession from "components/CurrentSession";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";


export default function SessionPage() {
  const { user, setRefreshSession } = useUserContext();

  useEffect(() => {
    if (!setRefreshSession) return;

    const interval = setInterval(() => {
      setRefreshSession((prevRefreshSession) => !prevRefreshSession);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return <div className="flex flex-col items-center justify-center h-full gap-5">
    <h1 className="text-5xl font-bold text-center font-serif">Your Session</h1>
    <div className="w-full">
      <p className="text-xl text-center text-slate-50 mb-3">Share this url with your friends for them to join!</p>
      <CopyInput text={`${BACKEND_HOST}/auth/login/${user?.id}`} />
    </div>
    <CurrentSession />
    <Button className="rounded-xl" asChild>
      <Link to={"/blendify"} className="text-xl">Let's Go!</Link>
    </Button>
  </div>;
}
