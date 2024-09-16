import { ReactNode, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useCurrentUserQuery } from "hooks/user";

export default function PrivatePage({ children }: { children: ReactNode }) {
    const { data: user } =  useCurrentUserQuery();
    const navigate = useNavigate();

    useEffect(() => {
        if (!user?.id) {
            navigate('/');
        }
    })

    return <>{children}</>
}