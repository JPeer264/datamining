import helper


def fetch(page=1):
    return helper.api_call("method=chart.gettopartists&limit=200&page={page}".format(page=page))


def save():
    this_dir = "./fetched_data/top_artists"
    artists_response = fetch()

    helper.ensure_dir(this_dir)

    total_user_pages = artists_response['artists']['@attr']['totalPages']

    helper.save_json(artists_response, this_dir + "/page_1.json")

    for i in range(0, int(total_user_pages)):
        page = i + 1

        if page == 1 or page > 20:
            continue

        artists_response = fetch(page)
        current_page = artists_response['artists']['@attr']['page']

        helper.save_json(
            artists_response,
            "{this_dir}/page_{page}.json".format(
                this_dir=this_dir, page=current_page)
        )


if __name__ == '__main__':
    save()
