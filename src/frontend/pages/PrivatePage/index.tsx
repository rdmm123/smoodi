import { useUserContext } from "contexts/UserContext";
import { ReactNode, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function PrivatePage({ children }: { children: ReactNode }) {
    const { user } =  useUserContext();
    const navigate = useNavigate();

    useEffect(() => {
        if (!user?.id) {
            navigate('/');
        }
    }, [])

    return <>{children}</>
}