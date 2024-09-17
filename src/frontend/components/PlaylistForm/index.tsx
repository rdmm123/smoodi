import { zodResolver } from "@hookform/resolvers/zod"
import { useForm, SubmitHandler } from "react-hook-form"
import { z } from "zod"
import { Shuffle, Loader2 } from "lucide-react"
import { useRef } from "react"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Toggle } from "@/components/ui/toggle"

import { User } from "services/api.types"
import { useCurrentUserQuery, useUserSessionQuery } from "hooks/user"

const getFormSchema = (session: User[]) => {
  return z.object({
    length: z.coerce.number({
      invalid_type_error: "Invalid value"
    })
    .gt(session.length, 'Playlist must have at least one song per person')
    .lte(500, "Playlist length can't exceed 500"),
    shuffle: z.boolean()
  })
}

interface PlaylistFormProps {
  onSubmit?(onSubmitArgs: OnSubmitArgs): void,
  allowCreate?: boolean
  isLoading?: boolean
}

export interface OnSubmitArgs {
  length: number,
  shuffle: boolean,
  create: boolean
}

export default function PlaylistForm({ onSubmit, allowCreate = false, isLoading = false }: PlaylistFormProps) {
  const { data: user } = useCurrentUserQuery();
  const { data: session } = useUserSessionQuery(user);

  if (!session) {
    return;
  }

  const formSchema = getFormSchema(session);
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      shuffle: true
    },
  })
  const createBtnRef = useRef(null);

  const onFormSubmit: SubmitHandler<z.infer<typeof formSchema>> = (values, event) => {
    if (!onSubmit) {
      console.log(values);
      return;
    }

    const nativeEvent = event?.nativeEvent as SubmitEvent;
    const onSubmitArgs = values as OnSubmitArgs;

    onSubmitArgs.create = nativeEvent.submitter === createBtnRef.current
    onSubmit(onSubmitArgs);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onFormSubmit)} className="flex gap-4 items-top justify-center flex-wrap">
        <FormField
          control={form.control}
          name="length"
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <Input className="border-2 border-my-green bg-my-green-100 text-my-purple w-96" type="number" placeholder="Playlist length" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="shuffle"
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <Toggle
                  pressed={field.value}
                  name={field.name}
                  id={field.name}
                  onPressedChange={field.onChange}
                  variant={"outline"}
                ><Shuffle /></Toggle>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          disabled={isLoading}
        >
          {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Preview
        </Button>
        {
          allowCreate &&
          <Button
            disabled={!allowCreate || isLoading}
            variant={"secondary"}
            ref={createBtnRef}
            type="submit"
          >
            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Create
          </Button>
        }
      </form>
    </Form>
  )
}
