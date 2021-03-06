from glob import glob
import numpy as np
import json
import csv
import re

import helper


class TagsGen:
    def __init__(self, no_artist_ref=False):
        self.tags_line = ""
        self.top_tags_line = ""
        self.tag_names = []
        self.artist_names = []
        self.artist_mbids = []
        self.no_artist_ref = no_artist_ref

        self.FETCHED_DATA = "./fetched_data/"
        self.SAVE_DIR = "./data/"
        self.FILENAME = "tags.txt"
        self.FILENAME_TOP_TAGS = "top_tags.txt"
        self.TOP_TAGS = 'top_tags'
        self.ARTISTS_META = 'artists_meta'
        self.ARTISTS_FILE = self.SAVE_DIR + "artists.txt"


    def compute(self):
        self.artist_names, self.artist_mbids = self.get_all_artists()
        self.tags_line = self.tag_array_to_line("init", self.get_tag_format())
        self.top_tags_line = self.tag_array_to_line("init", ['tag_ref', 'reach', 'taggings'])
        all_tags, top_tags = self.prepare_tags()

        for tag in all_tags:
            self.tags_line = self.tags_line + \
                self.tag_array_to_line(tag, self.get_tag_format())

        for tag in top_tags:
            self.top_tags_line = self.top_tags_line + \
                self.tag_array_to_line(tag, ['tag_ref', 'reach', 'taggings'])


    @staticmethod
    def get_tag_format():
        return ["name"]

    def get_all_artists(self):
        artist_names = []
        artist_mbid = []

        with open(self.ARTISTS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()

            for row in reader:
                artist_names.append(row[headers.index("name")])
                artist_mbid.append(row[headers.index("mbid")])

        return artist_names, artist_mbid

    def tag_array_to_line(self, tag="init", tag_format=[]):
        line = ""

        if tag == "":
            return ""

        for i, entry in enumerate(tag_format):
            temp_line = "%"

            if i == 0:
                temp_line = ""

            name = ""

            if tag == "init":
                name = entry
            else:
                name = re.sub(r'%*', '', tag[entry])

            line = line + temp_line + name

        return line + "\n"

    def get_tag_array(self, tag):
        name = tag['name'].encode('utf8')

        name = name.lower()
        name = re.sub(r'\W*', '', name)

        if name == "":
            return ""

        # make sure the tag name exists
        if name in self.tag_names:
            return ""

        self.tag_names.extend([name])

        return {
            'name': name,
        }


    def save(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME, 'w')

        to_write_file.write(self.tags_line)
        to_write_file.close()


    def save_top_tags(self):
        helper.ensure_dir(self.SAVE_DIR)

        to_write_file = open(self.SAVE_DIR + self.FILENAME_TOP_TAGS, 'w')

        to_write_file.write(self.top_tags_line)
        to_write_file.close()


    def prepare_tags(self):
        all_tags_array = []
        top_tags_array = []

        # loop over users top tags
        files = glob(self.FETCHED_DATA + self.TOP_TAGS + "/*.json")

        for file in files:
            file_payload = json.load(open(file))
            tags = file_payload['tags']['tag']

            for idx, tag in enumerate(tags):
                print str(idx) + ' of ' + str(len(tags))
                tag_array = self.get_tag_array(tag)

                if tag_array == "":
                    continue

                top_tags = {}
                top_tags['tag_ref'] = str(len(all_tags_array))
                top_tags['reach'] = str(tag['reach'])
                top_tags['taggings'] = str(tag['taggings'])
                top_tags_array.extend([top_tags])

                all_tags_array.extend([tag_array])

        # loop over artists meta
        files = glob(self.FETCHED_DATA + self.ARTISTS_META + "/*.json")

        for idx, file in enumerate(files):
            print str(idx) + ' of ' + str(len(files))
            file_payload = json.load(open(file))

            if 'error' in file_payload:
                continue

            tags = file_payload['artist']['tags']['tag']

            for tag in tags:
                tag_array = self.get_tag_array(tag)

                if tag_array == "":
                    continue

                all_tags_array.extend([tag_array])

        return all_tags_array, top_tags_array


if __name__ == '__main__':
    tagsGen = TagsGen()
    tagsGen.compute()
    tagsGen.save()
    tagsGen.save_top_tags()
