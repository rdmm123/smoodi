import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator
} from '@/components/ui/dropdown-menu';

import { ChevronDown, LogOut } from "lucide-react";

import { useCurrentUserQuery } from "hooks/user";
import {  getUserDisplayName } from "utils/user";
import UserAvatar from "./UserAvatar";

export default function UserDropdown() {
  const { data: user } = useCurrentUserQuery()

  if (!user) {
    return;
  }

  return <DropdownMenu>
    <DropdownMenuTrigger asChild>
      <Button variant={"ghost"} className='py-5 px-3'>
        <UserAvatar user={user} className="size-9 mr-2" />
        <ChevronDown />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuLabel>{getUserDisplayName(user)}</DropdownMenuLabel>
      <DropdownMenuSeparator className="bg-my-purple-800" />
      <DropdownMenuItem>
        <LogOut className="h-4 w-4 mr-2"></LogOut>
        <a href={BACKEND_HOST + "/auth/logout"}>Log Out</a>
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>;
}