import { useUserContext } from "contexts/UserContext";
import { useState } from "react";
import { createBlend } from "services/api";

import { Playlist as PlaylistType } from "services/api.types";
import Playlist from "components/Playlist";
import PlaylistForm, { OnSubmitArgs } from "components/PlaylistForm";
import PlaylistDialog from "components/Playlist/PlaylistDialog";
import ErrorMessage from "components/ErrorMessage";

export default function BlendifyPage() {
  const { user, session } = useUserContext();

  if (!user) { return }

  const blendUsers = [...session];
  blendUsers.push(user);

  const initialPlaylist: PlaylistType = {tracks: []}
  const [playlist, setPlaylist] = useState(initialPlaylist);

  const [isPlaylistDialogOpen, setIsPlaylistDialogOpen] = useState(false);
  
  const [apiError, setApiError] = useState('');
  
  const handleFormSubmit = async ({ length, create }: OnSubmitArgs) => {
    const playlistResponse = await createBlend(blendUsers, length, create);
    if (!playlistResponse.isSuccess) {
      return setApiError(playlistResponse.message || '')
    }

    if (create) {
      if (!playlistResponse.playlist.id) {
        return setApiError('There was an issue while creating your playlist. Please try again later.')
      }

      setIsPlaylistDialogOpen(true);
    }

    setPlaylist(playlistResponse.playlist);
  }

  return <>
    <div className="space-y-6">
      <h1 className="text-5xl font-bold mb-9 text-center font-serif">Make your Blend!</h1>
      <PlaylistForm onSubmit={handleFormSubmit} allowCreate={playlist.tracks.length > 0}/>
      { apiError &&  <ErrorMessage message={apiError} />}
      <Playlist tracks={playlist.tracks}/>
      <PlaylistDialog open={isPlaylistDialogOpen} setOpen={setIsPlaylistDialogOpen} playlist={playlist} />
    </div>
    {/* TODO: Add current session footer */}
  </>
}