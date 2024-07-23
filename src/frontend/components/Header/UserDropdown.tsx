import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu';
import {
  Avatar,
  AvatarFallback,
  AvatarImage
} from '@/components/ui/avatar';
import { ChevronDown, LogOut } from "lucide-react";

import { useUserContext } from "contexts/UserContext"

const getUserInitials = (fullName: string) => {
  const names = fullName.split(' ');

  return names
    .map(name => name[0].toUpperCase())
    .join('')
    .slice(0, 2);
}

export default function UserDropdown() {
  const { user } = useUserContext();

  if (!user) {
    return;
  }

  return <DropdownMenu>
    <DropdownMenuTrigger asChild>
      <Button variant={"ghost"} className='py-5 px-3'>
        <Avatar className='w-9 h-9 mr-2'>
          <AvatarImage src={user.image_url} />
          <AvatarFallback>{getUserInitials(user.name)}</AvatarFallback>
        </Avatar>
        <ChevronDown />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent>
      <DropdownMenuItem>
        <LogOut className="h-4 w-4 mr-2"></LogOut>
        <a href={BACKEND_HOST + "/auth/logout"}>Log Out</a>
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>;
} 