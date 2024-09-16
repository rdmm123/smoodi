import { useCurrentUserQuery, useUserSessionQuery } from "hooks/user";
import SessionUserCard from "./SessionUserCard";

import { ScrollArea } from "@/components/ui/scroll-area";

const SESSION_REFRESH_MS = 1000 * 2;

export default function CurrentSession() {
    const { data: user } = useCurrentUserQuery();
    const { data: session } = useUserSessionQuery(user, SESSION_REFRESH_MS);

    if (!user || !session) return;

    const allUsers = [user, ...session]
    // TODO: Add link to spotify for each user
    return <ScrollArea className="h-[26rem] w-full rounded-xl bg-my-purple-950">
      <div className="flex flex-wrap gap-4 justify-center p-4">
        {allUsers.map((user) => <SessionUserCard user={user} key={user.id} />)}
      </div>
    </ScrollArea>
}