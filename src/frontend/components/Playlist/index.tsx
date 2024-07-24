import { MouseEvent } from "react";

import { Track } from "services/api.types";
import Button from "components/Button/Button";
import TrackCard from "components/Playlist/TrackCard";

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

  return <div className="w-full space-y-3 p-3">
    {tracks.map((track) => <TrackCard track={track} key={track.uri}/>)}
  </div>
  // return <div className="p-8 my-5 rounded-xl outline outline-1 outline-slate-300">
  //   <h1 className="text-4xl mb-5">Your playlist</h1>
  //   <hr className="mb-5" />
  //   <ol className="list-decimal list-inside text-lg">
  //     {tracks.map((track) =>
  //       <li key={track.uri}>
  //         <a href={track.external_url} className="font-bold underline" target="_blank">{track.name}</a> - {track.user.email}</li>)}
  //   </ol>
  //   <hr className="my-5" />
  //   <div className="w-full text-end">
  //     <Button color='green' light={false} onClick={handleOnConfirm}>Confirm</Button>
  //   </div>
  // </div>
}