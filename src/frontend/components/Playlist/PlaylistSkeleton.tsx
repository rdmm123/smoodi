import { Skeleton } from "@/components/ui/skeleton"
import { ScrollArea } from "@/components/ui/scroll-area";

export function TrackCardSkeleton() {
  return <div className="flex items-center justify-between w-full bg-my-green-100 rounded-xl border-2 border-my-green p-2 text-my-purple">
    <div className="flex gap-3 w-1/2">
      <Skeleton className="aspect-square size-12 rounded-lg" />
      <div className="space-y-2 w-full">
        <Skeleton className="h-5 w-full" />
        <Skeleton className="h-5 w-2/3" />
      </div>
    </div>
    <div>
    <Skeleton className="h-12 w-12 rounded-full" />
    </div>
  </div>
}

export function PlaylistSkeleton() {
  return <ScrollArea className="h-[30rem] w-full">
    <div className="w-full space-y-3 px-3">
      <TrackCardSkeleton />
      <TrackCardSkeleton />
      <TrackCardSkeleton />
      <TrackCardSkeleton />
      <TrackCardSkeleton />
      <TrackCardSkeleton />
      <TrackCardSkeleton />
    </div>
</ScrollArea>
}