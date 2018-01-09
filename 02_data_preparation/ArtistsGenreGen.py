from glob import glob
import numpy as np
import csv
import re

try:
    import ujson as json
except ImportError:
    import json

import helper
from ArtistsGen import ArtistsGen


class ArtistsGenreGen:
    def __init__(self):
        self.artists_line = ""
        self.artists = []
        self.artist_names = []
        self.artist_mbids = []
        self.tag_to_artist = {}

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/"
        self.TAGS_FILE = self.SAVE_DIR + "tags.txt"
        self.FILENAME = "artists.txt"
        self.FILENAME_TAGS = "artists_with_tags.txt"
        self.ARTISTS_META = 'artists_meta'
        self.ARTISTS_FILE = self.SAVE_DIR + self.FILENAME

    def compute(self):
        self.artist_names, self.artist_mbids = self.get_all_artists()
        self.artists_line = self.artist_array_to_line("init")
        self.artists_tags_line = "artist_ref%tags_refs\n"
        self.get_tags()
        all_artists = self.prepare_artists()

        for idx, artist in enumerate(self.artists):
            print str(idx) + ' of ' + str(len(self.artists))
            mbid = artist['mbid']
            name = artist['name']

            ##
            # artist tags
            artist_tags = ""
            if not mbid == '':
                try:
                    artist_tags = self.tag_to_artist[mbid]
                except ValueError:
                    # not found but also name not in all_artists // --> no file found
                    if not name == '':
                        try:
                            artist_tags = self.tag_to_artist[name]
                        except ValueError:
                            pass

            if not idx == -1:
                self.artists_tags_line = self.artists_tags_line + \
                    str(idx) + artist_tags + "\n"

    @staticmethod
    def get_artist_format():
        artists_format = ArtistsGen.get_artist_format()

        artists_format.extend(['listeners', 'playcount'])

        return artists_format

    def get_tags(self):
        tag_ids = []
        tag_names = []

        with open(self.TAGS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()
            count = 0

            for row in reader:
                tag_ids.append(count)
                tag_names.append(row[headers.index("name")])
                count = count + 1

        self.tag_ids = tag_ids
        self.tag_names = tag_names

    def normalize_genres(self, tags, name, mbid):
        result = ""

        if len(tags) <= 0:
            return

        for tag in tags:
            name = tag['name']
            name = name.lower()
            name = re.sub(r'[\W%]*', '', name)

            if name == "":
                continue

            result = result + "%" + str(self.tag_names.index(name))

        key = name

        if not mbid == '':
            key = mbid

        if key == "":
            return

        self.tag_to_artist[key] = result


    def get_artist_array(self, artist):
        name = artist['name'].encode('utf8')
        mbid = ''
        listeners = artist['stats']['listeners'].encode('utf8')
        playcount = artist['stats']['playcount'].encode('utf8')

        if 'mbid' in artist:
            mbid = artist['mbid'].encode('utf8')

        self.normalize_genres(artist['tags']['tag'], name, mbid)

        return {
            'name': name,
            'mbid': mbid,
            'listeners': listeners,
            'playcount': playcount,
        }

    def artist_array_to_line(self, artist="init"):
        artist_format = self.get_artist_format()
        line = ""

        if artist == "":
            return ""

        for i, entry in enumerate(artist_format):
            temp_line = "%"

            if i == 0:
                temp_line = ""

            name = ""

            if artist == "init":
                name = entry
            if entry in artist:
                name = re.sub(r'%*', '', artist[entry])

            line = line + temp_line + name

        return line + "\n"

    def get_all_artists(self):
        artist_names = {}
        artist_mbid = {}

        with open(self.ARTISTS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()
            counter = 0

            for row in reader:
                name = row[headers.index("name")]
                name = re.sub(r'\s*', '', name)
                mbid = row[headers.index("mbid")]

                if not mbid == "":
                    artist_mbid[row[headers.index("mbid")]] = counter

                artist_names[name] = counter
                counter += 1

        return artist_names, artist_mbid

    def save(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME, 'w')

        to_write_file.write(self.artists_line)
        to_write_file.close()


if __name__ == '__main__':
    artistsGenreGen = ArtistsGenreGen()
    artistsGenreGen.compute()
    artistsGenreGen.save()
