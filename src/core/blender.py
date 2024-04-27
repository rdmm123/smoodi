"""
BLENDER LOGIC:
Each user has its song stack and song pool
    song stack -> the ones that are going in the playlist. initially of length = songs_per_user
    song pool -> the rest of the songs of the user's top.

So first off we get user's top {N * songs_per_user} tracks.
We split that top:
    the first {songs_per_user} will be the song stack
    the rest will be the song pool

For each iteration:
- pop the song at the top of each user's stack and
- for each song, check if song is repeated:
    if its not repeated: keep going
    if it's already on the playlist:
        - pop the song at the top of user's pool
        - pull in that song
        - pop the current top of user's stack
    if it's another user's current top:
        - one of the users will be the one putting the song in from their stack.
        - to choose this user:
            - check the user that has the lower songs_per_user
            - if both are the same: choose randomly
            - if not: choose the user with the greater songs_per_user
            - this way we make it a bit more fair for the users with less songs
        - for the rest, we will do the same as if the song were already on the playlist
- store the songs in an array
- keep going until all user stacks are empty
"""

import random
from collections.abc import Collection
from collections import deque

from core.client.base import User, Client, Track

DEFAULT_PLAYLIST_LENGTH = 100


class StackHandler:
    def __init__(self, stack: list[Track] = [], pool: list[Track] = []) -> None:
        self.stack = deque(stack)
        self.pool = deque(pool)
        self.track_amount = len(stack) + len(pool)

    def pull_from_pool(self) -> None:
        self.stack.append(self.pool.popleft())

    def pop_left_and_pull_from_pool(self) -> Track:
        self.pull_from_pool()
        return self.stack.popleft()


class Blender:
    _songs_per_user: int = 0
    playlist: list[Track] = []

    def __init__(
        self,
        client: Client,
        users: Collection[User],
        playlist_length: int = DEFAULT_PLAYLIST_LENGTH,
    ) -> None:
        self.users = {u.email: u for u in users}
        self.client = client
        self.playlist_length = playlist_length

        self._stacks_per_user: dict[str, StackHandler] = {}

        self._set_stacks_per_user()

    def _set_stacks_per_user(self) -> None:
        songs_per_user, extra_song_count = divmod(self.playlist_length, len(self.users))
        for i, user in enumerate(self.users):
            user_obj = self.users[user]

            songs = songs_per_user
            if i < extra_song_count:
                songs += 1

            all_tracks = user_obj.get_top_tracks(songs * 2)

            self._stacks_per_user[user] = StackHandler(
                all_tracks[:songs], all_tracks[songs:]
            )

    def _all_stacks_empty(self) -> bool:
        return all(len(sh.stack) == 0 for sh in self._stacks_per_user.values())
    
    def _get_remaining_users(self) -> set[str]:
        remaining_users: set[str] = set()

        for user in self._stacks_per_user:
            if len(self._stacks_per_user[user].stack) == 0:
                continue

            remaining_users.add(user)

        return remaining_users

    def blend(self) -> list[Track]:
        if len(self.playlist) == self.playlist_length:
            return self.playlist

        if self._all_stacks_empty():
            return self.playlist

        current_tops: dict[str, Track] = {}
        remaining_users = self._get_remaining_users()

        while len(remaining_users) > 0:
            current_user = remaining_users.pop()
            user_stack_handler = self._stacks_per_user[current_user]
            stack_top = user_stack_handler.stack.popleft()

            if stack_top in self.playlist:
                stack_top = user_stack_handler.pop_left_and_pull_from_pool()

            elif stack_top.name in current_tops:
                existing_track = current_tops[stack_top.name]
                # to make mypy stop crying
                assert existing_track.user is not None

                owner = existing_track.user
                owner_stack_handler = self._stacks_per_user[owner]

                if owner_stack_handler.track_amount < user_stack_handler.track_amount:
                    stack_top = user_stack_handler.pop_left_and_pull_from_pool()
                elif owner_stack_handler.track_amount > user_stack_handler.track_amount:
                    existing_track.user = current_user
                    owner_stack_handler.pull_from_pool()
                    remaining_users.add(owner)
                else:
                    new_owner = random.choice((owner, current_user))
                    if new_owner == current_user:
                        existing_track.user = current_user
                        owner_stack_handler
                        remaining_users.add(owner)
                    else:
                        user_stack_handler.pop_left_and_pull_from_pool()

            current_tops[stack_top.name] = stack_top

        self.playlist += [track for track in current_tops.values()]

        return self.blend()
