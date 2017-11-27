import helper


def fetch(page=1):
    return helper.api_call("method=chart.gettoptracks&limit=200&&page={page}".format(page=page))


def save():
    this_dir = "../fetched_data/top_tracks"
    tracks_response = fetch()

    helper.ensure_dir(this_dir)

    total_user_pages = tracks_response['tracks']['@attr']['totalPages']

    helper.save_json(tracks_response, this_dir + "/page_1.json")

    for i in range(0, int(total_user_pages)):
        page = i + 1

        if page == 1 | page > 10:
            pass

        tracks_response = fetch(page)
        current_page = tracks_response['tracks']['@attr']['page']

        helper.save_json(
            tracks_response,
            "{this_dir}/page_{page}.json".format(
                this_dir=this_dir, page=current_page)
        )


if __name__ == '__main__':
    save()
