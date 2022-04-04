# Module for Spotify related stuff
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from time import sleep


scope = "playlist-modify-private,user-modify-playback-state,playlist-read-private,user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_ID, client_secret=cred.client_SECRET,
                                               redirect_uri=cred.redirect_uri, scope=scope))
user_id = sp.current_user()["id"]


def create_amp():
    # Ask Spotify API for info on user's playlists
    results = sp.current_user_playlists()
    playlists = results["items"]

    # Check each playlist name to see if AMP already exists
    for playlist in playlists:
        name = playlist["name"]

        # If it exists, output its uri
        # print(name)
        if name == "AMP":
            return playlist["uri"]

    # If it doesn't exist, make it and output its uri
    return sp.user_playlist_create(user_id, "AMP", public=False, description="Adaptive Music Player Playlist")["uri"]


def generate_music(seed_tracks, energy, emax, emin, danceability, dmax, dmin, speechiness):

    # Get recommendation uris
    tracks = sp.recommendations(seed_tracks=seed_tracks, limit=75, target_energy=energy, max_energy=emax,
                                min_energy=emin, target_danceability=danceability, max_danceability=dmax,
                                min_danceability=dmin, target_speechiness=speechiness, min_popularity=70,
                                country="US")["tracks"]
    uris = []

    # Append recommendation uris to the output
    for track in tracks:
        uris.append(track["uri"])

    return uris


def pause():
    # Pause player
    try:
        sp.pause_playback()
    # Unless there is no active device
    except (spotipy.SpotifyException, TimeoutError):
        print("Something went wrong, please make sure you have Spotify open and have been listening to music within the"
              " past five minutes or so.")
        sleep(1.5)


def resume():
    # Getting info about current playback
    current_playback = sp.current_playback()

    # If there is no playback (aka no active session) then print error message
    if current_playback is None:
        print("\nThe session has timed out. "
              "You waited too long and now the Spotify API thinks there are no active devices.\n"
              "It is also possible that something else has gone wrong")
        return

    current_context = current_playback["context"]["uri"]
    current_song = {"uri": current_playback["item"]["uri"]}
    current_progress_ms = current_playback["progress_ms"]

    # Start playback at the song that was playing, at the timestamp it was paused at, in the playlist it was played from
    sp.start_playback(context_uri=current_context, offset=current_song, position_ms=current_progress_ms)


def play():
    amp_uri = create_amp()

    # Play playlist
    try:
        sp.start_playback(context_uri=amp_uri)
    # Unless there is no active device
    except (spotipy.SpotifyException, TimeoutError):
        print("Something went wrong, please make sure you have Spotify open and have been listening to music within the"
              " past five minutes or so.")
        sleep(1.5)


# Given the intensity number from 0 to 5, return a list of song ids which reflect that intensity
def fetch_music(intensity):

    # If fetch_music is passed a number that isn't 0, 1, 2, 3, 4, or 5, default to 2
    if intensity not in [0, 1, 2, 3, 4, 5]:
        intensity = 2

    seeds = None
    energy = {"min": None, "target": None, "max": None}
    dance = {"min": None, "target": None, "max": None}
    target_speechiness = None

    # Intensity 0/5: Calmest music, few vocals
    if intensity == 0:
        # Seeds are: The Penguins - Earth Angel, cloudcrush - mellow,
        #            Ever So Blue - Progress, The Beatles - Yesterday,
        #            Pink Floyd - Shine on You Crazy Diamond (Pts. 1-5)
        seeds = ["spotify:track:75Mwp7YsQRk0ZBq1lOdL2T", "spotify:track:7CVgHbVQmNtUVXKZOgonJK",
                 "spotify:track:6oJIMUBDopuFljMNBFrq9Z", "spotify:track:3BQHpFgAp4l80e1XslIjNI",
                 "spotify:track:6pnwfWyaWjQiHCKTiZLItr"]
        energy["target"] = 0.0
        energy["max"] = 0.4
        dance["target"] = 0.1
        dance["max"] = 0.5
        target_speechiness = 0.0

    # Intensity 1/5: Still calm, little pep
    if intensity == 1:
        # Seeds are: Neil Diamond - Sweet Caroline, Johnny Nash - I Can See Clearly Now,
        #            The Beatles - Blackbird, Kansas - Dust in the Wind,
        #            Grateful Dead - Althea
        seeds = ["spotify:track:6l7tK5SsMlN8a9ccgeIkpS", "spotify:track:0oCT5rVvMdPPUm0bxG7yzT",
                 "spotify:track:5jgFfDIR6FR0gvlA56Nakr", "spotify:track:6zeE5tKyr8Nu882DQhhSQI",
                 "spotify:track:7M7AwtGvWdMYudqx5Iuh1m"]
        energy["target"] = 0.3
        energy["max"] = 0.5
        dance["target"] = 0.4

    # Intensity 2/5: Little more energetic, more of a bop
    if intensity == 2:
        # Seeds are: Don McLean - American Pie, The Animals - House Of The Rising Sun,
        #            Marty Robbins - Big Iron, Ruel - Painkiller
        #            The Chords - Sh-Boom
        seeds = ["spotify:track:2QgWuCtBpNIpl5trmKCxRf", "spotify:track:7BY005dacJkbO6EPiOh2wb",
                 "spotify:track:0AQquaENerGps8BQmbPw14", "spotify:track:1abFkY2jm6KDFMZ7RD9YJh",
                 "spotify:track:1jeQT4ymqWO7TJr4Ei8NLz"]
        energy["target"] = 0.4
        energy["min"] = 0.3
        dance["target"] = 0.6

    # Intensity 3/5: Mid, has energy, but not too much, good vibes
    if intensity == 3:
        # Seeds are: Red Hot Chili Peppers - Snow (Hey Oh), Fleetwood Mac - The Chain,
        #            Tears For Fears - Everybody Wants To Rule The World, Redbone - Come and Get Your Love,
        #            Milky Chance - Stolen Dance
        seeds = ["spotify:track:2aibwv5hGXSgw7Yru8IYTO", "spotify:track:5e9TFTbltYBg2xThimr0rU",
                 "spotify:track:2GOGDZ9wAJbmznIstAxiU4", "spotify:track:7GVUmCP00eSsqc4tzj1sDD",
                 "spotify:track:6vECYJHxYmm3Ydt3fF01pE"]
        energy["target"] = 0.6
        energy["min"] = 0.5
        dance["target"] = 1.0

    # Intensity 4/5: Energetic, but still room to escalate
    if intensity == 4:
        # Seeds are: Tally Hall - Turn the Lights Off, The Beatles - I Want To Hold Your Hand,
        #            League of Legends & Nicki Taylor - Worlds Collide, The Human League - Don't You Want Me,
        #            Bea Miller - Playground
        seeds = ["spotify:track:3xpdefOloYCBXd3UR6MVyM", "spotify:track:4pbG9SUmWIvsROVLF0zF9s",
                 "spotify:track:6KMgPewrVRxzeFzRwkFa0M", "spotify:track:3L7RtEcu1Hw3OXrpnthngx",
                 "spotify:track:52iCFhfKpun0w0MewtTi1B"]
        energy["target"] = 0.8
        energy["min"] = 0.5
        energy["max"] = 0.85
        dance["target"] = 0.7

    # Intensity 5/5: Most energetic
    if intensity == 5:
        # Seeds are: The Living Tombstone - Lazy, Casey Edwards & Victor Borba - Bury The Light,
        #            Pentakill - Redemption, Jimmy Gnecco - It Has To Be This Way - Platinum Mix,
        #            Bring Me The Horizon - Can You Feel My Heart
        seeds = ["spotify:track:5jiq6gYgiuXHyymaAyWKfE", "spotify:track:6tUcFEXos6TGhESFlkAyCm",
                 "spotify:track:3voBp3LlT8uHeQJ1QNWr8K", "spotify:track:65yNr1EO2TOBEYCz45tuOf",
                 "spotify:track:1PInWkBARsxLyouDqa2GtF"]
        energy["target"] = 1.0
        energy["min"] = 0.8

    return generate_music(seeds, energy["target"], energy["max"], energy["min"], dance["target"], dance["max"],
                          dance["min"], target_speechiness)


def test_stuff():

    results = sp.current_user_playlists()["items"]
    for playlist in results:
        print(playlist["name"])

    # Getting audio features
    # uri = sp.playlist_items(playlist_id=create_amp(), fields="items(track.uri)")["items"][0]["track"]["uri"]
    # audio_features = sp.audio_features(uri)[0]

    # for item in audio_features:
    #    print(f"{item}: {audio_features[item]}")

    # Print the uris of tracks in AMP
    # print(sp.playlist_items(playlist_id=create_amp(), fields="items(track.uri)"))


# Given the list of songs, put those songs into a playlist and play it
def music_fusion(songs):

    # Make a playlist named "AMP" if there is not already one and save uri for later
    amp_uri = create_amp()

    # Cut off "spotify:playlist:" from the uri to get id
    amp_id = amp_uri[17:]

    # For each song in the list, put into AMP playlist replacing anything currently in it
    sp.playlist_replace_items(amp_id, songs)


def activate(intensity, delay):
    # Find music & put into playlist
    music_fusion(fetch_music(intensity))

    # Delay for x seconds and play
    sleep(delay)
    play()
