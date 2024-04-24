import { useUserContext } from "contexts/UserContext"

export default function CurrentSession() {
    const { session } = useUserContext();
    // TODO: Add link to spotify for each user
    return <div className="rounded-lg outline outline-1 outline-slate-200 p-5">
        <h1 className="text-xl font-bold text-green-500">Current session:</h1>
        <ul>
          {session.map((user) => <li key={user.email}>{user.email}</li>)}
        </ul>
      </div>
}