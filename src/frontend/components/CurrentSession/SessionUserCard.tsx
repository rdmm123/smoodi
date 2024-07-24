import React from "react";
import { Button } from "@/components/ui/button";
import { X } from "lucide-react";

import { User } from "services/api.types";
import { getUserDisplayName } from "utils/user";
import UserAvatar from "components/Header/UserAvatar";

interface SessionUserCardProps {
  user: User
}

export default function SessionUserCard({ user }: SessionUserCardProps): React.ReactElement {
  const removeUserFromSession = () => {
    // TODO
  }

  return <div className="bg-my-green-100 size-40 break-all rounded-xl border-4 border-my-green p-1 flex flex-col items-center justify-center text-my-purple gap-3 relative">
    <Button variant={"ghost"} className="absolute top-1 right-1 p-1 rounded-full h-auto" onClick={removeUserFromSession}>
      <X className="text-my-pink size-5" strokeWidth={3} />
    </Button>

    <UserAvatar user={user} className="size-14 outline outline-4 outline-my-purple-900" />
    <p className="text-center font-bold text-sm">{getUserDisplayName(user)}</p>
  </div>
}