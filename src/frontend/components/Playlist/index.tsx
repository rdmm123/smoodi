import { Track } from "services/api.types";

export default function Playlist({ tracks }: { tracks: Track[]}) {

    return <div className="p-5 my-5 rounded-xl outline outline-1 outline-slate-300">
        <h1 className="text-4xl mb-4">Your playlist</h1>
        <ol className="list-decimal list-inside text-lg">
            { tracks.map((track) => <li><span className="text-bold">{track.name}</span> - {track.user}</li>)}
        </ol>
    </div>
}