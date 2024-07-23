import React from "react";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Ban } from "lucide-react";

import { User } from "services/api.types";
import { getUserInitials, getUserDisplayName } from "utils/user";

interface SessionUserCardProps {
  user: User
}

export default function SessionUserCard({ user }: SessionUserCardProps): React.ReactElement {
  const removeUserFromSession = () => {
    // TODO
  }

  return <div className="bg-my-green-100 size-40 break-all rounded-xl border-4 border-my-green p-1 flex flex-col items-center justify-center text-my-purple gap-3 relative">
    <Button variant={"ghost"} className="absolute top-1 right-1 p-1 rounded-full h-auto" onClick={removeUserFromSession}>
      {/* TODO: Allow removing user from session */}
      <Ban className="text-my-pink size-5" strokeWidth={3} />
    </Button>

    <Avatar className='size-14 outline outline-4 outline-my-purple-900'>
      <AvatarImage src={user.image_url} />
      <AvatarFallback>{getUserInitials(user)}</AvatarFallback>
    </Avatar>
    <p className="text-center font-bold text-sm">{getUserDisplayName(user)}</p>
  </div>
}