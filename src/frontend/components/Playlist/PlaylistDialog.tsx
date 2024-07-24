import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
  } from "@/components/ui/alert-dialog"
import { Playlist } from "services/api.types";

interface PlaylistDialogProps {
    open: boolean;
    setOpen(open: boolean): void;
    playlist: Playlist;
}

export default function PlaylistDialog({ open, setOpen, playlist }: PlaylistDialogProps) {
    return <AlertDialog open={open} onOpenChange={setOpen}>
    <AlertDialogContent className="bg-my-green-100 border-4 border-my-green text-my-purple">
        <AlertDialogHeader>
        <AlertDialogTitle>Playlist created!</AlertDialogTitle>
        <AlertDialogDescription className="text-my-purple">
            Your playlist was successfully created, you can view
            it <a className="underline text-my-blue" href={playlist.external_url} target="_blank">here.</a> You
            can close this page now.
        </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
        <AlertDialogAction>Accept</AlertDialogAction>
        </AlertDialogFooter>
    </AlertDialogContent>
    </AlertDialog>
}