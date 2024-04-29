import React, { createContext, useState, useContext, useEffect } from "react";
import { fetchCurrentUser, fetchUserSession } from "services/api";
import { User } from "services/api.types";

interface UserData {
  user: User | null
  session: User[],
  refreshSession: boolean | null
  setRefreshSession: React.Dispatch<React.SetStateAction<boolean>> | null
}

const initialContext: UserData = { user: null, session: [], refreshSession: null, setRefreshSession: null };
const UserContext = createContext(initialContext)

export function UserContextProvider({ children } : { children: React.ReactNode }) {

  const initialUser: User = { name: '', email: '', id: ''}
  const [user, setUser] = useState(initialUser);

  const initialSession: User[] = []
  const [session, setSession] = useState(initialSession);
  const [refreshSession, setRefreshSession] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
        const user = await fetchCurrentUser();
        if (user) setUser(user);
    }
    fetchUser();
  }, [])

  useEffect(() => {
    const fetchSession = async () => {
      const session = await fetchUserSession(user);
      if (session) setSession(session)
    }
    if (user.id) {
      fetchSession()
    }
  }, [refreshSession, user])

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