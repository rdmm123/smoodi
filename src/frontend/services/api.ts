import { UserResponse } from "./api.types";

const API_URL = BACKEND_HOST + '/api';

export const fetchCurrentUser = async () => {
    const response = await fetch(API_URL + '/users/me', {credentials: 'include'})

    const userResponse: UserResponse = await response.json()
    return userResponse.user;
}