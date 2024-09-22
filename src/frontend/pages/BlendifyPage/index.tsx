import { useState } from "react";

import { previewBlend, createBlend } from "services/api";
import { useCurrentUserQuery, useUserSessionQuery } from "hooks/user";
import { useMutation } from "@tanstack/react-query";

import { Playlist as PlaylistType, User } from "services/api.types";
import Playlist from "components/Playlist";
import PlaylistForm, { OnPreviewArgs } from "components/PlaylistForm";
import PlaylistDialog from "components/Playlist/PlaylistDialog";
import ErrorMessage from "components/ErrorMessage";
import SessionFooter from "components/CurrentSession/SessionFooter";
import { PlaylistSkeleton } from "components/Playlist/PlaylistSkeleton";

interface PreviewBlendMutationArgs extends OnPreviewArgs {
  mainUser: User,
  session: User[]
}

export default function BlendifyPage() {
  const { data: user } = useCurrentUserQuery();
  const { data: session } = useUserSessionQuery(user);

  const previewBlendMutation = useMutation({
    mutationKey: ["blender", "preview"],
    mutationFn: ({ mainUser, session, length, shuffle }: PreviewBlendMutationArgs) =>
      previewBlend(mainUser, session, length, shuffle),
    onSuccess: (data) => {
      setPlaylist(data.playlist);
      setApiError("")
    },
    onError: (error) => {
      if (error.name === 'TypeError') {
        setApiError("An unknown error has ocurred. Please try again later.")
      } else {
        setApiError(error.message)
      }
    }
  });

  const createBlendMutation = useMutation({
    mutationKey: ["blender", "create"],
    mutationFn: () => createBlend(user!, session!),
    onSuccess: (data) => {
      setPlaylist(data.playlist);
      setApiError("")
      setIsPlaylistDialogOpen(true);
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

  return <div className="flex flex-col justify-between items-center h-full w-full gap-3">
    <div className="flex flex-col justify-center grow gap-10 w-full py-5">
      <h1 className="text-5xl font-bold text-center font-serif">Make your Smoodi!</h1>
      <PlaylistForm
        onPreview={(args) => previewBlendMutation.mutate({mainUser: user!, session: session!, ...args})}
        onCreate={createBlendMutation.mutate}
        allowCreate={playlist.tracks.length > 0}
        isLoading={previewBlendMutation.isPending}/>
      { apiError &&  <ErrorMessage message={apiError} />}
      { previewBlendMutation.isPending
        ? <PlaylistSkeleton />
        : <Playlist tracks={playlist.tracks}/>}

      <PlaylistDialog open={isPlaylistDialogOpen} setOpen={setIsPlaylistDialogOpen} playlist={playlist} />
    </div>

    <SessionFooter />
  </div>
}