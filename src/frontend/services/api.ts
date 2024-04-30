import { BlendResponse, User, UserResponse, UserSessionResponse, Playlist } from "./api.types";

const API_URL = BACKEND_HOST + '/api';

export const fetchCurrentUser = async () => {
    const response = await fetch(API_URL + '/users/me', {credentials: 'include'})

    if (!response.ok) {
        return null
    }

    const userResponse: UserResponse = await response.json()
    
    return userResponse.user;
}

export const fetchUserSession = async ({ id }: User) => {
    const response = await fetch(`${API_URL}/users/${id}/session`)

    if (!response.ok) {
        return null
    }

    const userSessionResponse: UserSessionResponse = await response.json()
    
    return userSessionResponse.session;
}

export const createBlend = async (users: User[], playlistLength: number, create: boolean = false) => {
    const response = await fetch(`${API_URL}/blender/blend`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify({
            users: users.map(user => user.id),
            playlist_length: playlistLength,
            create: create
        })
    })

    if (!response.ok) {
        return { tracks: [] }
    }

    const blendResponse: BlendResponse = await response.json()
    const playlist: Playlist = { ...blendResponse.playlist, tracks: [] };
    
    playlist.tracks = blendResponse.playlist.tracks.map(track => ({
        ...track,
        user: users.filter(user => user.id === track.user)[0]
    }))

    return playlist;
}