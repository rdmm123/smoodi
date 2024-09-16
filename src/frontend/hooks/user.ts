import { useQuery } from '@tanstack/react-query';
import { fetchCurrentUser, fetchUserSession } from 'services/api';
import { User } from 'services/api.types';

// Fetch the current user
function useCurrentUserQuery() {
  return useQuery({
    queryKey: ['users', 'me'],
    queryFn: fetchCurrentUser,
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 10
  });
}

function useUserSessionQuery(user: User | null | undefined, refetchInterval: number | false = false) {
  return useQuery({
    queryKey: ['users', user?.id, 'session'],
    queryFn: () => user && fetchUserSession(user),
    staleTime: 1000 * 60 * 10,
    enabled: !!user,
    refetchInterval
  });
}

export {
  useCurrentUserQuery,
  useUserSessionQuery
}