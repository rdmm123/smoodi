import UserAvatar from "components/Header/UserAvatar";
import { Track } from "services/api.types";

export default function TrackCard ({ track }: { track: Track}) {
    return <div className="flex items-center justify-between w-full bg-my-green-100 rounded-xl border-2 border-my-green p-2 text-my-purple">
        <div className="flex gap-3">
          <img className="aspect-square size-12 rounded-lg" src={track.cover_art}/>
          <div>
              <a className="text-xl font-bold hover:underline" target="_blank" href={track.external_url}>{track.name}</a>
              <p className="font-medium">
                  {track.artists.map((artist, idx, artists) => (
                    <a key={artist.url} href={artist.url} target="_blank" className="hover:underline">
                          {artist.name + (idx < artists.length - 1 ? ', ' : '')}
                    </a>
                  ))}
              </p>
          </div>
        </div>
        <div>
          <UserAvatar user={track.user}/>
        </div>
    </div>
}