import { ReactNode, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useCurrentUserQuery } from "hooks/user";

export default function PrivatePage({ children }: { children: ReactNode }) {
    const { data: user, isPending } =  useCurrentUserQuery();
    const navigate = useNavigate();


    useEffect(() => {
        if (!user?.id && !isPending) {
            navigate('/');
        }
    })

    if (isPending) {
        return <p>Loading...</p>
    }

    return <>{children}</>
}