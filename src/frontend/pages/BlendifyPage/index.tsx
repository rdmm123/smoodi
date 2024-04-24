import { useUserContext } from "contexts/UserContext";
import { FormEvent, useEffect, useState} from "react";
import { createBlend } from "services/api";

import { Track } from "services/api.types";
import Button from "components/Button/Button";
import Playlist from "components/Playlist";
import CurrentSession from "components/CurrentSession";

export default function BlendifyPage() {
  const { user, session } = useUserContext();

  const initialPlaylist: Track[] = []
  const [playlist, setPlaylist] = useState(initialPlaylist);

  const [blendLoading, setBlendLoading] = useState(false);

  const handleFormSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const blendUserIds = session.map((sessionUser) => sessionUser.id);

    if (!user) return;

    blendUserIds.push(user.id)
    const createdPlaylist = await createBlend(blendUserIds, 100);
    setPlaylist(createdPlaylist)
  }

  return <>
    <h1 className="text-5xl font-bold mb-9 text-center">Let's make a blend!</h1>
    <div className="flex justify-around w-3/4">
      <form onSubmit={handleFormSubmit} className="flex gap-5 items-start justify-center p-5">
        <input
          name="playlistLength"
          type="number"
          className="text-lg p-2 bg-slate-50 border outline-2 outline-slate-300 rounded-lg min-w-64"
          max={500}
          min={1}
          placeholder="Playlist length"/>
        <Button color="green" light={false} type="submit" className="text-2xl" >Go!</Button>
      </form>
      <CurrentSession />
    </div>
      {playlist.length > 0 && <Playlist tracks={playlist}/>}
  </>
}