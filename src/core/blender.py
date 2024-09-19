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

from src.core.client.base import User, Client, Track

DEFAULT_PLAYLIST_LENGTH = 100


class StackHandler:
    def __init__(
        self, stack: Collection[Track] = [], pool: Collection[Track] = []
    ) -> None:
        self.stack = deque(stack)
        self.pool = deque(pool)
        self.track_amount = len(stack) + len(pool)

    def pull_from_pool(self) -> None:
        self.stack.append(self.pool.popleft())


class Blender:
    def __init__(
        self,
        client: Client,
        users: Collection[User],
        playlist_length: int = DEFAULT_PLAYLIST_LENGTH,
    ) -> None:
        self.playlist: list[Track] = []
        self._playlist_per_user: dict[str, list[Track]] = {}

        self.users = {}
        for u in users:
            assert u.id is not None
            self.users[u.id] = u
            self._playlist_per_user[u.id] = []

        self.client = client
        self.playlist_length = playlist_length

        self._stacks_per_user: dict[str, StackHandler] = {}

        self._set_stacks_per_user()

        self._remaining_users: set[str] = set()

    def _set_stacks_per_user(self) -> None:
        songs_per_user, extra_song_count = divmod(self.playlist_length, len(self.users))
        for i, user in enumerate(self.users):
            user_obj = self.users[user]

            songs = songs_per_user
            if i < extra_song_count:
                songs += 1

            all_tracks = self.client.get_top_tracks_from_user(user_obj, songs * 2)

            self._stacks_per_user[user] = StackHandler(
                all_tracks[:songs], all_tracks[songs:]
            )

    def _all_stacks_empty(self) -> bool:
        return all(len(sh.stack) == 0 for sh in self._stacks_per_user.values())

    def _get_remaining_users(self) -> set[str]:
        for user in self._stacks_per_user:
            if len(self._stacks_per_user[user].stack) == 0:
                continue

            self._remaining_users.add(user)

        return self._remaining_users

    def _track_in_playlist(self, track: Track) -> bool:
        for p_track in self.playlist:
            if p_track.uri == track.uri:
                return True

        return False

    def blend(self, shuffle: bool = False) -> list[Track]:
        if len(self.playlist) == self.playlist_length:
            return self.join_playlist(shuffle)

        if self._all_stacks_empty():
            return self.join_playlist(shuffle)

        current_tops: dict[str, Track] = {}
        remaining_users = self._get_remaining_users()

        while len(remaining_users) > 0:
            current_user = remaining_users.pop()
            user_stack_handler = self._stacks_per_user[current_user]
            stack_top = user_stack_handler.stack.popleft()

            if self._track_in_playlist(stack_top):
                user_stack_handler.pull_from_pool()
                remaining_users.add(current_user)
                continue

            if stack_top.uri in current_tops:
                existing_track = current_tops[stack_top.uri]
                # to make mypy stop crying
                assert existing_track.user is not None

                owner = existing_track.user
                owner_stack_handler = self._stacks_per_user[owner]

                if owner_stack_handler.track_amount > user_stack_handler.track_amount:
                    user_stack_handler.pull_from_pool()
                    remaining_users.add(current_user)
                elif owner_stack_handler.track_amount < user_stack_handler.track_amount:
                    existing_track.user = current_user
                    owner_stack_handler.pull_from_pool()
                    remaining_users.add(owner)
                else:
                    new_owner = random.choice((owner, current_user))
                    if new_owner == current_user:
                        existing_track.user = current_user
                        owner_stack_handler.pull_from_pool()
                        remaining_users.add(owner)
                    else:
                        user_stack_handler.pull_from_pool()
                        remaining_users.add(current_user)

                continue

            current_tops[stack_top.uri] = stack_top

        for track in current_tops.values():
            assert track.user
            self.playlist.append(track)
            self._playlist_per_user[track.user].append(track)

        return self.blend(shuffle)

    def join_playlist(self, shuffle: bool) -> list[Track]:
        if not shuffle:
            return self.playlist

        songs_per_user, extra_song_count = divmod(self.playlist_length, len(self.users))
        total_count = songs_per_user + extra_song_count

        playlist = []
        shuffled_playlist_per_user = list(self._playlist_per_user.values())

        for sub_playlist in shuffled_playlist_per_user:
            random.shuffle(sub_playlist)

        for i in range(total_count):
            for sub_playlist in shuffled_playlist_per_user:
                try:
                    song = sub_playlist[i]
                except IndexError:
                    continue

                playlist.append(song)

        return playlist