import numpy as np
import csv


class Tags:
    def __init__(self):
        self.DATA = './data/'
        self.TAGS_FILE = self.DATA + 'tags.txt'
        self.TOP_TAGS_FILE = self.DATA + 'top_tags.txt'

        self.tag_ids = []
        self.tag_names = []
        self.top_tags = np.array([])

    def prepare_tags(self):
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


    def read_top_tags(self):
        top_tags = np.array([])

        with open(self.TOP_TAGS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='%')
            headers = reader.next()

            for row in reader:
                if len(top_tags) == 0:
                    top_tags = np.array([row])
                else:
                    top_tags = np.append(top_tags, [row], axis=0)

        print ''


    def get_tag_name(self, tag_ref):
        return self.tag_names[tag_ref]


if __name__ == '__main__':
    tags = Tags()
    tags.prepare_tags()
    tags.read_top_tags()
