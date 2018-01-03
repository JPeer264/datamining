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

class FillArtists:
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
        self.artists, self.artist_names, self.artist_mbids = self.get_all_artists()
        self.artists_line = self.artist_array_to_line("init")
        self.artists_tags_line = "artist_ref%tags_refs\n"
        self.get_tags()
        all_artists = self.prepare_artists()

        for idx, artist in enumerate(self.artists):
            print str(idx) + ' of ' + str(len(self.artists))
            mbid = artist['mbid']
            name = artist['name']
            artist_to_merge = {}

            ##
            # fill artists
            if (not mbid == '') and (mbid in all_artists):
                artist_to_merge = all_artists[mbid]

            # not found but also name not in all_artists // --> no file found
            if (not name == '') and (name in all_artists):
                artist_to_merge = all_artists[name]

            artist_copy = artist.copy()
            artist_copy.update(artist_to_merge)

            self.artists_line = self.artists_line + \
                self.artist_array_to_line(artist_copy)

            idx = -1

            if (not mbid == '') and (mbid in self.artist_mbids):
                idx = self.artist_mbids.index(mbid)

            # not found but also name not in all_artists // --> no file found
            if (not name == '') and (name in self.artist_mbids):
                idx = self.artist_mbids.index(name)


            ##
            # artist tags
            artist_tags = ""
            if (not mbid == '') and (mbid in self.tag_to_artist):
                artist_tags = self.tag_to_artist[mbid]

            # not found but also name not in all_artists // --> no file found
            if (not name == '') and (name in self.tag_to_artist):
                artist_tags = self.tag_to_artist[name]

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


    def normalize_tags(self, tags, name, mbid):
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


    def get_all_artists(self):
        artists_format = ArtistsGen.get_artist_format()
        artist_names = []
        artist_mbid = []
        artists = []

        with open(self.ARTISTS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()

            for row in reader:
                artist = {}

                artist_names.append(row[headers.index("name")])
                artist_mbid.append(row[headers.index("mbid")])

                for rowName in artists_format:
                    artist[rowName] = row[headers.index(rowName)]

                artists.append(artist)

        return artists, artist_names, artist_mbid


    def get_artist_array(self, artist):
        name = artist['name'].encode('utf8')
        mbid = ''
        listeners = artist['stats']['listeners'].encode('utf8')
        playcount = artist['stats']['playcount'].encode('utf8')

        if 'mbid' in artist:
            mbid = artist['mbid'].encode('utf8')

        self.normalize_tags(artist['tags']['tag'], name, mbid)

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


    def prepare_artists(self):
        all_artist_object = {}

        files = glob(self.FETCHED_DATA + self.ARTISTS_META + "/*.json")

        for idx, file in enumerate(files):
            print str(idx) + ' of ' + str(len(files))
            file_payload = json.load(open(file))

            if 'error' in file_payload:
                continue

            artist = file_payload['artist']
            artist_array = self.get_artist_array(artist)
            key = artist_array['name']

            if not artist_array['mbid'] == '':
                key = artist_array['mbid']

            all_artist_object[key] = artist_array

        return all_artist_object


    def save(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME, 'w')

        to_write_file.write(self.artists_line)
        to_write_file.close()


    def saveTags(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME_TAGS, 'w')

        to_write_file.write(self.artists_tags_line)
        to_write_file.close()


if __name__ == '__main__':
    fillArtists = FillArtists()
    fillArtists.compute()
    fillArtists.save()
    fillArtists.saveTags()
