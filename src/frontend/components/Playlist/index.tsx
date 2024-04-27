import { MouseEvent } from "react";

import { Track } from "services/api.types";
import Button from "components/Button/Button";

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

    return <div className="p-8 my-5 rounded-xl outline outline-1 outline-slate-300">
        <h1 className="text-4xl mb-5">Your playlist</h1>
        <hr className="mb-5"/>
        <ol className="list-decimal list-inside text-lg">
            { tracks.map((track) => <li key={track.uri}><span className="font-bold">{track.name}</span> - {track.user}</li>)}
        </ol>
        <hr className="my-5"/>
        <div className="w-full text-end">
            <Button color='green' light={false} onClick={handleOnConfirm}>Confirm</Button>
        </div>
    </div>
}