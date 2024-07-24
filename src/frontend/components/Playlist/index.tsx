import { MouseEvent } from "react";

import { Track } from "services/api.types";
import Button from "components/Button/Button";
import TrackCard from "components/Playlist/TrackCard";
import { ScrollArea } from "@/components/ui/scroll-area";

interface PlaylistProps {
  tracks: Track[],
  onConfirm?: Function
}

export default function Playlist({ tracks, onConfirm }: PlaylistProps) {
  const handleOnConfirm = (e: MouseEvent) => {
    e.preventDefault();

    if (onConfirm) {
      onConfirm(e);
    }
  }

  return <ScrollArea className="h-[30rem] w-full">
    <div className="w-full space-y-3 px-3">
      {tracks.map((track) => <TrackCard track={track} key={track.uri}/>)}
    </div>
  </ScrollArea>
}