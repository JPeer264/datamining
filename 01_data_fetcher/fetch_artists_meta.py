from glob import glob
import csv
import sys

import helper


def fetch_artist(artist):
    return helper.api_call("method=artist.getinfo&artist={artist}".format(artist=artist))


def fetch_mbid(mbid):
    return helper.api_call("method=artist.getinfo&mbid={mbid}".format(mbid=mbid))


def read_artists():
    file = './data/artists.txt'

    with open(file, 'r') as f:
        artist_names = []
        artist_mbids = []

        reader = csv.reader(f, delimiter='%')
        headers = reader.next()

        for row in reader:
            artist_names.append(row[headers.index("name")])
            artist_mbids.append(row[headers.index("mbid")])

    return artist_names, artist_mbids


def save():
    this_dir = "./fetched_data/artists_meta"
    artist_names, artist_mbids = read_artists()
    helper.ensure_dir(this_dir)

    for idx, mbid in enumerate(artist_mbids):
        if idx < int(sys.argv[1]):
            continue

        lala = True

        while (lala):
            print 'Fetch ' + str(idx) + ' of ' + str(len(artist_mbids))
            try:
                if not mbid == '':
                    artist_response = fetch_mbid(mbid)
                else:
                    artist_response = fetch_artist(artist_names[idx])

                if artist_response == {}:
                    continue

                helper.save_json(artist_response, this_dir + "/{idx}.json".format(idx=idx))
                lala = False
            except IOError:
                print 'retry'
                pass



if __name__ == '__main__':
    save()
