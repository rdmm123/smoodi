import { useUserContext } from "contexts/UserContext";
import { useState, FormEvent, MouseEvent} from "react";
import { createBlend } from "services/api";

import { Playlist as PlaylistType, Track } from "services/api.types";
import Playlist from "components/Playlist";
import CurrentSession from "components/CurrentSession";

import PlaylistForm from "components/PlaylistForm";

export default function BlendifyPage() {
  const { user, session } = useUserContext();

  if (!user) {
    return
  }

  const blendUserIds = session.map((sessionUser) => sessionUser.id);
  blendUserIds.push(user.id)

  const initialPlaylist: PlaylistType = {tracks: []}
  const [playlist, setPlaylist] = useState(initialPlaylist);
  const isPlaylistCreated = !!playlist.id;

  const [previewLoading, setPreviewLoading] = useState(false);
  const [blendLoading, setBlendLoading] = useState(false);
  
  const handleFormSubmit = async ({ formData }) => {
    const previewPlaylist = await createBlend(blendUserIds, parseInt(formData.playlistLength));
    setPlaylist(previewPlaylist);
  }

  const handlePlaylistConfirm = async(e: MouseEvent) => {    
    e.preventDefault();

    const createdPlaylist = await createBlend(blendUserIds, playlist.tracks.length, true);
    if (createdPlaylist.id) {
      setPlaylist(createdPlaylist);
    }
  }

  return <>
    <h1 className="text-5xl font-bold mb-9 text-center">Let's make a blend!</h1>
    <div className="flex justify-around w-3/4">
      <PlaylistForm onSubmit={handleFormSubmit} />
      <CurrentSession />
    </div>
      {(playlist.tracks.length > 0 && !isPlaylistCreated) &&
        <Playlist tracks={playlist.tracks} onConfirm={handlePlaylistConfirm}/>}
      {
        isPlaylistCreated &&
        <div>
          Playlist Created, <a href={playlist.external_url}>link</a>
        </div>
      }
  </>
}