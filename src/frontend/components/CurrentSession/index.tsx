import { useCurrentUserQuery, useUserSessionQuery } from "hooks/user";
import SessionUserCard from "./SessionUserCard";
import { deleteFromUserSession } from "services/api";
import { User } from "services/api.types";

import { ScrollArea } from "@/components/ui/scroll-area";
import { useMutation, useQueryClient } from "@tanstack/react-query";

const SESSION_REFRESH_MS = 1000 * 2;

export default function CurrentSession() {
    const { data: user } = useCurrentUserQuery();
    const { data: session } = useUserSessionQuery(user, SESSION_REFRESH_MS);

    if (!user) { return }

    const queryClient = useQueryClient();

    const deleteMutation = useMutation({
      mutationKey: ["users", user?.id, "session", "delete"],
      mutationFn: (toDelete: User) => {
        return deleteFromUserSession(user, toDelete)
      },
      onSuccess: (data) => {
        queryClient.setQueryData(["users", user?.id, "session"], data.session)
      }
    })

    if (!user || !session) return;

    const allUsers = [user, ...session]
    // TODO: Add link to spotify for each user
    return <ScrollArea className="h-[26rem] w-full rounded-xl bg-my-purple-950">
      <div className="flex flex-wrap gap-4 justify-center p-4">
        {allUsers.map((user) => <SessionUserCard user={user} key={user.id} onUserDelete={deleteMutation.mutate} />)}
      </div>
    </ScrollArea>
}