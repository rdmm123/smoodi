export interface Artist {
    name: string
    url: string
}

export interface Track {
    name: string
    external_url: string
    uri: string
    artists: Artist[]
    album: string
    cover_art: string
    preview: string
    user: string | null
}

export interface User {
    id: string
    name: string
    email: string
}

export interface UserResponse {
    user: User
}

export interface UserSessionResponse {
    session: User[]
}

export interface Playlist {
    tracks: Track[]
    id?: string
    href?: string
    uri?: string
    external_url?: string
    name?: string
    description?: string
    owner?: string
    public?: boolean
    collaborative?: boolean
}

export interface BlendResponse {
    playlist: Playlist
}
