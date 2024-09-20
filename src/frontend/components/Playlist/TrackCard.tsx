import UserAvatar from "components/Header/UserAvatar";
import { Track } from "services/api.types";

export default function TrackCard ({ track }: { track: Track}) {
    return <div className="flex items-center justify-between w-full bg-my-green-100 rounded-xl border-2 border-my-green p-2 text-my-purple">
        <div className="flex gap-3 items-center">
          <img className="aspect-square size-12 rounded" src={track.cover_art}/>
          <div className="flex flex-col">
              <a className="text-xl font-bold hover:underline" target="_blank" href={track.external_url}>{track.name}</a>
              <span className="font-medium">
                  {track.artists.map((artist, idx, artists) => (
                    <a key={artist.url} href={artist.url} target="_blank" className="hover:underline">
                          {artist.name + (idx < artists.length - 1 ? ', ' : '')}
                    </a>
                  ))}
              </span>
          </div>
        </div>
        <div>
          <UserAvatar user={track.user}/>
        </div>
    </div>
}