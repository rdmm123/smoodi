import { BlendResponse, User, UserResponse, UserSessionResponse } from "./api.types";

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

export const createBlend = async (userIds: string[], playlistLength: number) => {
    const response = await fetch(`${API_URL}/blender/blend`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
          },
        body: JSON.stringify({
            users: userIds,
            playlist_length: playlistLength
        })
    })

    if (!response.ok) {
        return []
    }

    const blendResponse: BlendResponse = await response.json()
    return blendResponse.playlist;
}