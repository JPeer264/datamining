1. First fetch artists, tags and tracks
    1. `./fetcher/fetch_top_artists.py`
    1. `./fetcher/fetch_top_tracks.py`
    1. `./fetcher/fetch_top_tags.py`
    1. `./fetcher/fetch_users_top_artists.py`
    1. `./fetcher/fetch_users_recent_tracks.py`
    1. `./fetcher/fetch_users_top_tracks.py`

1. Generate Files
    1. `./data_preparation/AristsGen`
    1. `./data_preparation/TracksGen` (depending on `./data/artists.txt`)
    1. `./data_preparation/UserRecentTracksGen` (depending on `./data/tracks.txt`)
    1. `./data_preparation/UserTopTracksGen` (depending on `./data/tracks.txt`)

1. Fetch Data Again
    1. `./fetcher/fetch_artists_meta.py` (depending on `./data/artists.txt`)

1. Generate Files Again
    1. `./data_preperation/TagsGen.py` (depending on `./fetched_data/artists_meta/*.json`)
    1. `./data_preperation/FillArtists.py` (depending on `./fetched_data/artists_meta/*.json`)

# Notes

- Every page of `user_recent_tracks` starts with the value `nowplaying: true`
- Tags to lower case and remove [ -] to combine e.g. Hip hop, hip hop and hip-hop
