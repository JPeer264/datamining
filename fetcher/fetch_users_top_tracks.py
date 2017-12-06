import helper


def fetch(user, page=1):
    return helper.api_call("method=user.gettoptracks&limit=200&user={user}&page={page}".format(user=user, page=page))

def save(username):
    this_dir = "./fetched_data/user_top_tracks/{username}".format(
        username=username)
    user_tracks_response = fetch(username)

    helper.ensure_dir(this_dir)

    total_user_pages = user_tracks_response['toptracks']['@attr']['totalPages']

    helper.save_json(user_tracks_response, this_dir + "/page_1.json")

    for i in range(0, int(total_user_pages)):
        page = i + 1

        if page == 1 or page > 10:
            continue

        user_tracks_response = fetch(username, page)
        current_page = user_tracks_response['toptracks']['@attr']['page']

        helper.save_json(
            user_tracks_response,
            "{this_dir}/page_{page}.json".format(
                this_dir=this_dir, page=current_page)
        )


if __name__ == '__main__':
    save('jpeer264')