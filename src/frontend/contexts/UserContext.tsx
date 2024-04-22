import React, { createContext, useState, useContext, useEffect } from "react";
import { fetchCurrentUser } from "services/api";
import { User } from "services/api.types";

interface UserData {
  user: User | null
  session: string[],
  refreshSession: boolean | null
  setRefreshSession: React.Dispatch<React.SetStateAction<boolean>> | null
}

const initialContext: UserData = { user: null, session: [], refreshSession: null, setRefreshSession: null };
const UserContext = createContext(initialContext)

export function UserContextProvider({ children } : { children: React.ReactNode }) {

  const initialUser: User = { name: '', email: '', top_tracks: []}
  const [user, setUser] = useState(initialUser);

  useEffect(() => {
    const fetchUser = async () => {
        const user = await fetchCurrentUser();
        setUser(user);
    }
    fetchUser();
  }, [])

  const initialSession: string[] = []
  const [session, setSession] = useState(initialSession);
  const [refreshSession, setRefreshSession] = useState(false);

  return (
    <UserContext.Provider
      value={{
        user,
        session,
        refreshSession,
        setRefreshSession
      }}>
        {children}
    </UserContext.Provider>
  )
}

export function useUserContext() {
  const context = useContext(UserContext);

  return context
}