import { FormEvent, useRef } from "react";
import Button from "components/Button/Button";

export interface OnSubmitArgs {
  e: FormEvent,
  formData: { playlistLength: string }
}

export default function PlaylistForm({ onSubmit }: { onSubmit?: Function }) {
  const lengthInputRef = useRef<HTMLInputElement>(null);

  const handleFormSubmit = (e: FormEvent) => {
    e.preventDefault();

    const formData = {
      playlistLength: lengthInputRef.current?.value ?? '',
    }

    if (onSubmit) {
      const onSubmitArgs: OnSubmitArgs = { e, formData }
      onSubmit(onSubmitArgs)
    }
  }

  return <form onSubmit={handleFormSubmit} className="flex gap-5 items-start justify-center p-5">
    <input
      name="playlistLength"
      type="number"
      className="text-lg p-2 bg-slate-50 border outline-2 outline-slate-300 rounded-lg min-w-64"
      max={500}
      min={1}
      ref={lengthInputRef}
      placeholder="Playlist length" />
    <Button color="green" light={false} type="submit" className="text-2xl" >Go!</Button>
  </form>
}