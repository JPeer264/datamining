import helper

# USER RELATED


def fetch_users_meta(user):
    return helper.api_call("method=user.getinfo&user={user}".format(user=user))

# def fetch_users_loved_tracks(user):
#     return helper.api_call("method=user.getlovedtracks&limit=200&user={user}".format(user=user))

# FOR MAINSTREAMINESS

# def fetch_top_tags(page=1):
#     return helper.api_call("method=chart.gettoptags&limit=200&page={page}".format(page=page))

# NEEDED META DATA

def fetch_artists_meta(artist):
    return helper.api_call("method=artist.getinfo&limit=200&artist={artist}".format(artist=artist))


if __name__ == '__main__':
    print fetch_users_meta('jpeer264')
