export interface Artist {
    name: string
    url: string
}

export interface Track {
    name: string
    url: string
    artists: Artist[]
    album: string
    cover_art: string
    preview: string
    user: string | null
}

export interface User {
    name: string
    email: string
    top_tracks: Track[]
}

export interface UserResponse {
    user: User
}