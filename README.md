1. First fetch artists, tags and tracks
    1. `./01_data_fetcher/fetch_top_artists.py`
    1. `./01_data_fetcher/fetch_top_tracks.py`
    1. `./01_data_fetcher/fetch_top_tags.py`
    1. `./01_data_fetcher/fetch_users_top_artists.py`
    1. `./01_data_fetcher/fetch_users_recent_tracks.py`
    1. `./01_data_fetcher/fetch_users_top_tracks.py`

1. Generate Files
    1. `./02_data_preparation/UsersGen.py`
    1. `./02_data_preparation/AristsGen.py` (depending on `./data/users.txt`)
    1. `./02_data_preparation/TracksGen.py` (depending on `./data/artists.txt`)
    1. `./02_data_preparation/UserRecentTracksGen.py` (depending on `./data/tracks.txt`)
    1. `./02_data_preparation/UserTopTracksGen.py` (depending on `./data/tracks.txt`)
    1. `./02_data_preparation/UserTopArtistGen.py` (depending on `./data/tracks.txt`)

1. Fetch Data Again
    1. `./01_data_fetcher/fetch_artists_meta.py` (depending on `./data/artists.txt`)

1. Generate Files Again
    1. `./02_data_preparation/TagsGen.py` (depending on `./fetched_data/artists_meta/*.json`)
    1. `./02_data_preparation/FillArtists.py` (depending on `./fetched_data/artists_meta/*.json`)

1. Generate processed data to analyze
    1. `./03_data_processing/top_tags-user_top_artists.py` - Get top tags and count how often a user heard that artist (user top artists)

# Notes

- Every page of `user_recent_tracks` starts with the value `nowplaying: true`
- Tags to lower case and remove [ -] to combine e.g. Hip hop, hip hop and hip-hop

# Presentation

- Ansatz
- Was gemacht
- Ergebnisse
- Was gelernt
- Deutsch/English
- Report in English (4-8 Seiten)
  - Guideline: Nachimplementierung sollte nach dem Lesen möglich sein (nachvollziehbar)
