import { useUserContext } from "contexts/UserContext";
import { useEffect } from "react";
import { useState } from "react";
import { Track } from "services/api.types";
import { createBlend } from "services/api";
import Playlist from "components/Playlist";

import CopyInput from "components/CopyInput";
import Button from "components/Button/Button";

export default function BlenderPage() {
  const { user, session, setRefreshSession } = useUserContext();
  const [blendLoading, setBlendLoading] = useState(false)

  const initialPlaylist: Track[] = []
  const [playlist, setPlaylist] = useState(initialPlaylist)

  const handleBlendOnClick = async () => {
    const createdPlaylist = await createBlend(session.map((user) => user.id), 100)
    setPlaylist(createdPlaylist)
  }

  useEffect(() => {
    if (!setRefreshSession) return;

    const interval = setInterval(() => {
      setRefreshSession((prevRefreshSession) => !prevRefreshSession);
    }, 2000);
  
    return () => clearInterval(interval);
  }, []);

  return <>
      <h1 className="text-5xl font-bold mb-5 text-center">Let's create a Blend!</h1>
      <div className="flex gap-10 justify-center">
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
            <li>Wait for them to log in. Check current session right here:</li>
            <li>When everyone has logged in, press the big button:</li>
          </ol>
          <Button color="green" light={false} className="shrink-0" onClick={handleBlendOnClick}>Blendify</Button>
        </div>
        <div className="rounded-lg outline outline-1 outline-slate-200 p-5">
          <h1 className="text-xl font-bold text-green-500">Current session:</h1>
          <ul>
            {session.map((user) => <li>{user.email}</li>)}
          </ul>
        </div>
      </div>
      {playlist.length > 0 && 
          <Playlist tracks={playlist}/>}
    </>;
}
