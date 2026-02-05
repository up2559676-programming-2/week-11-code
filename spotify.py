from dataclasses import dataclass, field
import datetime
import random
from typing import ClassVar, Self

_CDN_ROOT: str = "https://i.scdn.co"


@dataclass
class Song:
    all_songs: ClassVar[list[Self]] = []

    title: str
    artist: "Artist"
    album: "Album"
    duration: datetime.timedelta
    cover_art_id: str = "default_id"
    play_count: int = field(default_factory=lambda: random.randrange(1_000, 100_000))

    def __post_init__(self):
        self.all_songs.append(self)

    def __str__(self) -> str:
        return f"{self.title.ljust(20)} | {self.artist.display_name.ljust(15)} | {format_duration(self.duration)}"


@dataclass
class Album:
    name: str
    primary_artist: "Artist"
    release_date: datetime.datetime
    cover_art_id: str
    songs: list[Song] = field(default_factory=list)

    @property
    def artists(self) -> set["Artist"]:
        return {song.artist for song in self.songs}

    @property
    def duration(self):
        return sum((song.duration for song in self.songs), datetime.timedelta())

    @property
    def cover_art_link(self) -> str:
        return f"{_CDN_ROOT}/image/{self.cover_art_id}"


class User:
    def __init__(self, username: str, profile_picture_id: str) -> None:
        self.username: str = username
        self.display_name: str = username
        self.profile_picture_id: str = profile_picture_id
        self.playlists: list[Playlist] = []

    @property
    def profile_picture_link(self) -> str:
        return f"{_CDN_ROOT}/image/{self.profile_picture_id}"

    def find_song(self, title: str) -> list[Song]:
        return [song for song in Song.all_songs if song.title == title]

    def create_playlist(self, name: str) -> "Playlist":
        playlist = Playlist(name, self)
        self.playlists.append(playlist)
        print(f"INFO: Created playlist '{name}' for {self.display_name}")
        return playlist


class Artist(User):
    def __init__(self, name: str, profile_picture_id: str, banner_art_id: str) -> None:
        super().__init__(name.replace(" ", "_").lower(), profile_picture_id)
        self.display_name: str = name
        self.banner_art_id: str = banner_art_id
        self.albums: dict[str, Album] = {}
        self.about_me = ""

    @property
    def monthly_listens(self) -> int:
        total = 0
        for album in self.albums.values():
            total += sum(song.play_count for song in album.songs)
        return total

    @property
    def banner_art_link(self) -> str:
        return f"{_CDN_ROOT}/image/{self.banner_art_id}"

    def add_album(self, album: Album):
        self.albums[album.name] = album

    def add_song(self, album_name: str, song: Song):
        if album_name not in self.albums:
            raise ValueError(f"Album '{album_name}' not found")
        self.albums[album_name].songs.append(song)


class Playlist:
    def __init__(self, name: str, creator: User) -> None:
        self.name = name
        self.creator = creator
        self._songs: list[Song] = []

    def __str__(self) -> str:
        header = f"\nPlaylist: {self.name} (by {self.creator.display_name})\n"
        line = "-" * 50 + "\n"
        titles = f"{'#':<3} {'Title':<20} | {'Artist':<15} | {'Duration':<8}\n"

        content = ""
        for idx, song in enumerate(self._songs, 1):
            content += f"{idx:<3} {song}\n"

        footer = f"\nTotal Tracks: {len(self._songs)}"
        footer += f"\nTotal Duration: {format_duration(self.total_duration)}\n"
        return header + line + titles + line + content + line + footer

    @property
    def songs(self) -> list[Song]:
        return self._songs

    @property
    def total_duration(self) -> datetime.timedelta:
        return sum((s.duration for s in self._songs), datetime.timedelta())

    def add_song(self, song: Song):
        self._songs.append(song)
        print(f"INFO: Added '{song.title}' to {self.name}")

    def remove_song(self, song_title: str):
        initial_count = len(self._songs)
        self._songs = [s for s in self._songs if s.title.lower() != song_title.lower()]
        if len(self._songs) < initial_count:
            print(f"INFO: Removed '{song_title}' from {self.name}")
        else:
            print(f"WARN: Song '{song_title}' not found.")

    def move_song(self, current_pos: int, new_pos: int):
        """Moves a song from current_pos to new_pos (1-indexed)"""
        if 1 <= current_pos <= len(self._songs) and 1 <= new_pos <= len(self._songs):
            song = self._songs.pop(current_pos - 1)
            self._songs.insert(new_pos - 1, song)
        else:
            print("ERROR: Invalid positions provided.")


def format_duration(td: datetime.timedelta) -> str:
    """Format timedelta as MM:SS"""
    total_seconds = int(td.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"


def test():
    print("=" * 60)

    # Create artists
    print("\n[1] Creating Artists...")
    artist1 = Artist("Taylor Swift", "ts_profile_001", "ts_banner_001")
    artist1.about_me = "Award-winning singer-songwriter"

    artist2 = Artist("The Weeknd", "tw_profile_002", "tw_banner_002")
    artist2.about_me = "R&B and pop artist"

    print(f"   Created: {artist1.display_name} (@{artist1.username})")
    print(f"   Created: {artist2.display_name} (@{artist2.username})")

    # Create albums
    print("\n[2] Creating Albums...")
    album1 = Album(
        name="1989",
        primary_artist=artist1,
        release_date=datetime.datetime(2014, 10, 27),
        cover_art_id="1989_cover",
    )
    artist1.add_album(album1)

    album2 = Album(
        name="After Hours",
        primary_artist=artist2,
        release_date=datetime.datetime(2020, 3, 20),
        cover_art_id="after_hours_cover",
    )
    artist2.add_album(album2)

    print(f"   {artist1.display_name}: '{album1.name}'")
    print(f"   {artist2.display_name}: '{album2.name}'")

    # Create songs
    print("\n[3] Creating Songs...")
    song1 = Song(
        "Shake It Off",
        artist1,
        album1,
        datetime.timedelta(minutes=3, seconds=39),
        "shake_cover",
    )
    song2 = Song(
        "Blank Space",
        artist1,
        album1,
        datetime.timedelta(minutes=3, seconds=51),
        "blank_cover",
    )
    song3 = Song(
        "Style",
        artist1,
        album1,
        datetime.timedelta(minutes=3, seconds=51),
        "style_cover",
    )

    song4 = Song(
        "Blinding Lights",
        artist2,
        album2,
        datetime.timedelta(minutes=3, seconds=20),
        "blinding_cover",
    )
    song5 = Song(
        "Save Your Tears",
        artist2,
        album2,
        datetime.timedelta(minutes=3, seconds=35),
        "tears_cover",
    )

    album1.songs.extend([song1, song2, song3])
    album2.songs.extend([song4, song5])

    print(f"   Added {len(album1.songs)} songs to '{album1.name}'")
    print(f"   Added {len(album2.songs)} songs to '{album2.name}'")

    # Test album properties
    print("\n[4] Testing Album Properties...")
    print(f"   Album: {album1.name}")
    print(f"   Duration: {format_duration(album1.duration)}")
    print(f"   Artists in album: {', '.join(a.display_name for a in album1.artists)}")
    print(f"   Cover art: {album1.cover_art_link}")

    # Test artist monthly listens
    print("\n[5] Testing Artist Monthly Listens...")
    print(f"   {artist1.display_name}: {artist1.monthly_listens:,} plays")
    print(f"   {artist2.display_name}: {artist2.monthly_listens:,} plays")

    # Create users
    print("\n[6] Creating Users...")
    user1 = User("music_lover_42", "user_profile_001")
    user1.display_name = "Alex Johnson"

    user2 = User("beatmaster", "user_profile_002")
    user2.display_name = "Sam Chen"

    print(f"   Created: {user1.display_name} (@{user1.username})")
    print(f"   Created: {user2.display_name} (@{user2.username})")

    # Create playlists
    print("\n[7] Creating Playlists...")
    playlist1 = user1.create_playlist("Road Trip Vibes")
    playlist2 = user1.create_playlist("Workout Energy")
    playlist3 = user2.create_playlist("Chill Evening")

    # Add songs to playlists
    print("\n[8] Adding Songs to Playlists...")
    playlist1.add_song(song1)
    playlist1.add_song(song4)
    playlist1.add_song(song2)
    playlist1.add_song(song5)

    playlist2.add_song(song4)
    playlist2.add_song(song1)

    playlist3.add_song(song3)
    playlist3.add_song(song5)
    playlist3.add_song(song2)

    # Test duplicate detection
    print("\n[9] Testing Duplicate Detection...")
    playlist1.add_song(song1)  # Should warn

    # Display playlist
    print("\n[10] Displaying Playlist...")
    print(playlist1)

    # Test playlist operations
    print("\n[11] Testing Playlist Operations...")
    print(f"   Moving song from position 2 to position 1 in '{playlist1.name}'")
    playlist1.move_song(2, 1)
    print(playlist1)

    print(f"\n   Removing 'Blank Space' from '{playlist1.name}'")
    playlist1.remove_song("Blank Space")

    print("\n   Attempting to remove non-existent song...")
    playlist1.remove_song("Nonexistent Song")

    # Test song search
    print("\n[12] Testing Song Search...")
    found_songs = user1.find_song("Style")
    print(f"   Search for 'Style': Found {len(found_songs)} result(s)")
    for song in found_songs:
        print(f"      - {song}")

    # Display user's playlists
    print("\n[13] User Playlist Summary...")
    print(f"   {user1.display_name} has {len(user1.playlists)} playlist(s):")
    for pl in user1.playlists:
        print(
            f"      - '{pl.name}' ({len(pl.songs)} songs, {format_duration(pl.total_duration)})"
        )

    print(f"\n   {user2.display_name} has {len(user2.playlists)} playlist(s):")
    for pl in user2.playlists:
        print(
            f"      - '{pl.name}' ({len(pl.songs)} songs, {format_duration(pl.total_duration)})"
        )

    # Test all songs tracking
    print("\n[14] Total Songs in System...")
    print(f"   Total songs created: {len(Song.all_songs)}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test()
