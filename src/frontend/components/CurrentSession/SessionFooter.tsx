import UserAvatar from "components/Header/UserAvatar";
import { Link } from "react-router-dom";
import { Pencil } from "lucide-react";
import { Button } from "@/components/ui/button";

import { useUserContext } from "contexts/UserContext"

export default function SessionFooter() {
    const { session, user } = useUserContext();
    
    if (!user) {
        return;
    }
    
    const allUsers = [user, ...session]
    return <div className="flex items-center gap-3 max-w-full">
        <p>Current<br/>Session</p>
        <div className="bg-my-blue-200 border-x-4 border-t-4 border-my-blue min-w-72 text-my-purple rounded-t-xl p-2 flex items-center gap-3 justify-between">
        <div className="flex gap-2 flex-wrap">
            {allUsers.map((user) => <UserAvatar className="size-8" user={user}/>)}
        </div>
        <Button variant={"ghost"} className="p-1 rounded-lg h-auto" asChild>
            <Link to={"/session"}><Pencil className="text-my-blue" /></Link>
        </Button>
        </div>
    </div>
}