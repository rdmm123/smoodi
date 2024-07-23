import { useUserContext } from "contexts/UserContext"
import SessionUserCard from "./SessionUserCard";

import { ScrollArea } from "@/components/ui/scroll-area";

export default function CurrentSession() {
    const { session } = useUserContext();
    // TODO: Add link to spotify for each user
    return <ScrollArea className="h-[26rem] w-full rounded-xl bg-my-purple-950">
      <div className="flex flex-wrap gap-4 justify-center p-4">
        {session.map((user) => <SessionUserCard user={user} key={user.id} />)}
      </div>
    </ScrollArea>
}