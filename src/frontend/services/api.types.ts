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