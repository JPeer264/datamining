1. First fetch artists and trags
    1. `./fetcher/fetch_top_artists.py`
    1. `./fetcher/fetch_top_tracks.py`
    1. `./fetcher/fetch_users_top_artists.py`
    1. `./fetcher/fetch_users_recent_tracks.py`
    1. `./fetcher/fetch_users_top_tracks.py`

1. Generate Files
    1. `./data_preparation/AristsGen`
    1. `./data_preparation/TracksGen` (depending on `./data/artists.txt`)
    1. `./data_preparation/UserTracksGen` (depending on `./data/tracks.txt`)

1. Fetch Data Again
    1. `./fetcher/fetch_
