import { User, UserResponse, UserSessionResponse } from "./api.types";

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
    const response = await fetch(`${API_URL}/users/${id}/session`, {credentials: 'include'})

    if (!response.ok) {
        return null
    }

    const userSessionResponse: UserSessionResponse = await response.json()
    
    return userSessionResponse.session;
}