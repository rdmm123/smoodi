import { useUserContext } from "contexts/UserContext";
import { useEffect } from "react";
import CopyInput from "components/CopyInput";
import LinkButton from "components/Button/LinkButton";
import CurrentSession from "components/CurrentSession";


export default function SessionPage() {
  const { user, setRefreshSession } = useUserContext();

  useEffect(() => {
    if (!setRefreshSession) return;

    const interval = setInterval(() => {
      setRefreshSession((prevRefreshSession) => !prevRefreshSession);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return <>
    <h1 className="text-5xl font-bold mb-10 text-center font-serif">Your Session</h1>
    <p className="text-xl text-center text-slate-50 mb-3">Share this url with your friends for them to join!</p>
    <CopyInput text={`${BACKEND_HOST}/auth/login/${user?.id}`} />
    
    {/* <div className="flex gap-10 justify-center">
      <div className="flex flex-col gap-5">
        <p className="text-2xl">Just follow these few steps and we'll be done in no time:</p>
        <ol className="text-xl list-decimal marker:font-bold marker:text-green-500 marker:text-xl space-y-3">
          <li>Have friends (or a girlfriend, or familiy, or anything) that use Spotify</li>
          <li>
            <div className="flex items-center gap-3">
              <span>Share this link with them:</span>
              <CopyInput text={`${BACKEND_HOST}/auth/login/${user?.id}`} className="grow" />
            </div>
          </li>
          <li>Wait for them to log in</li>
          <li>When everyone has logged in, press the big button:</li>
        </ol>
        <LinkButton to="/blendify" color="green" light={false} className="text-center text-4xl self-center">Blendify</LinkButton>
      </div>
      <CurrentSession></CurrentSession>
    </div> */}
  </>;
}
