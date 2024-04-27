import { useUserContext } from "contexts/UserContext";
import { useState, FormEvent, MouseEvent} from "react";
import { createBlend } from "services/api";

import { Playlist as PlaylistType, Track } from "services/api.types";
import Button from "components/Button/Button";
import Playlist from "components/Playlist";
import CurrentSession from "components/CurrentSession";

export default function BlendifyPage() {
  const { user, session } = useUserContext();

  if (!user) {
    return
  }

  const blendUserIds = session.map((sessionUser) => sessionUser.id);
  blendUserIds.push(user.id)

  const initialPlaylist: PlaylistType = {tracks: []}
  const [playlist, setPlaylist] = useState(initialPlaylist);

  const [previewLoading, setPreviewLoading] = useState(false);
  const [blendLoading, setBlendLoading] = useState(false);
  const [isPlaylistCreated, setIsPlaylistCreated] = useState(false);

  const handleFormSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const previewPlaylist = await createBlend(blendUserIds, 100);
    setPlaylist(previewPlaylist);
    setIsPlaylistCreated(false);
  }

  const handlePlaylistConfirm = async(e: MouseEvent) => {    
    e.preventDefault();
    const createdPlaylist = await createBlend(blendUserIds, 100, true);
    if (createdPlaylist.id) {
      setIsPlaylistCreated(true);
      setPlaylist(createdPlaylist);
    }
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
      {(playlist.tracks.length > 0 && !isPlaylistCreated) && <Playlist tracks={playlist.tracks} onConfirm={handlePlaylistConfirm}/>}
      {
        isPlaylistCreated &&
        <div>
          Playlist Created, <a href={playlist.external_url}>link</a>
        </div>
      }
  </>
}