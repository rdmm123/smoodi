import { useUserContext } from "contexts/UserContext";
import { useState,  MouseEvent} from "react";
import { createBlend } from "services/api";

import { Playlist as PlaylistType } from "services/api.types";
import Playlist from "components/Playlist";
import CurrentSession from "components/CurrentSession";

import PlaylistForm, { OnSubmitArgs } from "components/PlaylistForm";
import ErrorMessage from "components/ErrorMessage";

export default function BlendifyPage() {
  const { user, session } = useUserContext();

  if (!user) { return }

  const blendUsers = [...session];
  blendUsers.push(user);

  const initialPlaylist: PlaylistType = {tracks: []}
  const [playlist, setPlaylist] = useState(initialPlaylist);
  const isPlaylistCreated = !!playlist.id;
  
  const [apiError, setApiError] = useState('');

  // const [previewLoading, setPreviewLoading] = useState(false);
  // const [blendLoading, setBlendLoading] = useState(false);
  
  const handleFormSubmit = async ({ length }: OnSubmitArgs) => {
    const previewPlaylistResponse = await createBlend(blendUsers, length);
    if (!previewPlaylistResponse.isSuccess) {
      return setApiError(previewPlaylistResponse.message || '')
    }
    setPlaylist(previewPlaylistResponse.playlist);
  }

  const handlePlaylistConfirm = async(e: MouseEvent) => {    
    e.preventDefault();

    const createdPlaylistResponse = await createBlend(blendUsers, playlist.tracks.length, true);
    if (!createdPlaylistResponse.isSuccess) {
      setApiError(createdPlaylistResponse.message ?? '')
      return;
    }

    const createdPlaylist = createdPlaylistResponse.playlist;
    if (createdPlaylist.id) {
      setPlaylist(createdPlaylist);
    }
  }

  return <>
    { apiError &&  <ErrorMessage message={apiError} />}
    <h1 className="text-5xl font-bold mb-9 text-center font-serif">Make your Blend!</h1>
    <PlaylistForm onSubmit={handleFormSubmit} />
    {/* <h1 className="text-5xl font-bold mb-9 text-center">Let's make a blend!</h1>
    <div className="flex justify-around w-3/4">
      <PlaylistForm onSubmit={handleFormSubmit} />
      <CurrentSession />
    </div>
      {(playlist.tracks.length > 0 && !isPlaylistCreated) &&
        <Playlist tracks={playlist.tracks} onConfirm={handlePlaylistConfirm}/>}
      {
        isPlaylistCreated &&
        <div>
          Playlist Created, <a className="underline text-green-500" href={playlist.external_url} target="_blank">link</a>
        </div>
      } */}
  </>
}