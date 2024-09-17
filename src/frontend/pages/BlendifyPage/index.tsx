import { useState } from "react";

import { createBlend } from "services/api";
import { useCurrentUserQuery, useUserSessionQuery } from "hooks/user";
import { useMutation } from "@tanstack/react-query";

import { Playlist as PlaylistType, User } from "services/api.types";
import Playlist from "components/Playlist";
import PlaylistForm, { OnSubmitArgs } from "components/PlaylistForm";
import PlaylistDialog from "components/Playlist/PlaylistDialog";
import ErrorMessage from "components/ErrorMessage";
import SessionFooter from "components/CurrentSession/SessionFooter";
import { PlaylistSkeleton } from "components/Playlist/PlaylistSkeleton";

interface CreateBlendMutationArgs extends OnSubmitArgs {
  blendUsers: User[]
}

export default function BlendifyPage() {
  const { data: user } = useCurrentUserQuery();
  const { data: session } = useUserSessionQuery(user);

  const createBlendMutation = useMutation({
    mutationKey: ["blend"],
    mutationFn: ({ blendUsers, length, create }: CreateBlendMutationArgs) =>
      createBlend(blendUsers, length, create),
    onSuccess: (data, variables) => {
      setPlaylist(data.playlist);
      setApiError("")
      if (variables.create && data.playlist.id) {
        setIsPlaylistDialogOpen(true);
      }
    },
    onError: (error) => {
      if (error.name === 'TypeError') {
        setApiError("An unknown error has ocurred. Please try again later.")
      } else {
        setApiError(error.message)
      }
    }
  });

  const [playlist, setPlaylist] = useState<PlaylistType>({tracks: []});

  const [isPlaylistDialogOpen, setIsPlaylistDialogOpen] = useState(false);

  const [apiError, setApiError] = useState('');

  if (!user || !session) { return }

  const blendUsers = [user, ...session];

  return <div className="flex flex-col justify-between items-center h-full w-full gap-3">
    <div className="flex flex-col justify-center grow gap-10 w-full py-5">
      <h1 className="text-5xl font-bold text-center font-serif">Make your Blend!</h1>
      <PlaylistForm
        onSubmit={(args) => createBlendMutation.mutate({blendUsers, ...args})}
        allowCreate={playlist.tracks.length > 0}
        isLoading={createBlendMutation.isPending}/>
      { apiError &&  <ErrorMessage message={apiError} />}
      { createBlendMutation.isPending
        ? <PlaylistSkeleton />
        : <Playlist tracks={playlist.tracks}/>}

      <PlaylistDialog open={isPlaylistDialogOpen} setOpen={setIsPlaylistDialogOpen} playlist={playlist} />
    </div>

    <SessionFooter />
  </div>
}