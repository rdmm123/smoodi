import { BlendResponse, User, UserResponse, UserSessionResponse, Playlist, ErrorResponse } from "./api.types";

const API_URL = BACKEND_HOST + '/api';

export const fetchCurrentUser = async () => {
    const response = await fetch(API_URL + '/users/me', { credentials: 'include' })

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

export const previewBlend = async (
    mainUser: User,
    session: User[],
    playlistLength: number,
    shuffle: boolean = false) => {
    const response = await fetch(`${API_URL}/blender/preview`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            main_user: mainUser.id,
            session: session.map(user => user.id),
            playlist_length: playlistLength,
            shuffle
        })
    })

    if (!response.ok) {
        const errorResponse: ErrorResponse = await response.json()
        throw Error(`Ooops! Something went wrong: ${errorResponse.message}. Please try again later.`)
    }

    const blendResponse: BlendResponse = await response.json()
    const playlist: Playlist = { ...blendResponse.playlist, tracks: [] };

    const users = [mainUser, ...session];
    playlist.tracks = blendResponse.playlist.tracks.map(track => ({
        ...track,
        user: users.filter(user => user.id === track.user)[0]
    }))

    return { playlist };
}

export const createBlend = async (mainUser: User, session: User[]) => {
    const response = await fetch(`${API_URL}/blender/create`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({user: mainUser.id})
    })

    if (!response.ok) {
        const errorResponse: ErrorResponse = await response.json();
        throw Error(`Ooops! Something went wrong: ${errorResponse.message}. Please try again later.`);
    }

    const blendResponse: BlendResponse = await response.json()
    const playlist: Playlist = { ...blendResponse.playlist, tracks: [] };

    const users = [mainUser, ...session];
    playlist.tracks = blendResponse.playlist.tracks.map(track => ({
        ...track,
        user: users.filter(user => user.id === track.user)[0]
    }))

    return { playlist };
}

export const deleteFromUserSession = async (owner: User, to_delete: User) =>  {
    const response = await fetch(`${API_URL}/users/${owner.id}/session/${to_delete.id}`, {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
        }
    })

    if (!response.ok) {
        const errorResponse: ErrorResponse = await response.json()
        throw Error(`Ooops! Something went wrong: ${errorResponse.message}. Please try again later.`)
    }

    const newSession: UserSessionResponse = await response.json();
    return newSession;
}
