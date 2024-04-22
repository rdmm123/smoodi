const API_URL = BACKEND_HOST + '/api';

interface CurrentUserResponse {
    current_user: string
}
export const fetchCurrentUser = async () => {
    const response = await fetch(API_URL + '/current_user', {credentials: 'include'})

    const currentUserResponse: CurrentUserResponse = await response.json()
    return currentUserResponse.current_user
}