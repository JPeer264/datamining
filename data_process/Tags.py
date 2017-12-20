import csv


class Tags:
    def __init__(self):
        self.DATA = './data/'
        self.TAGS_FILE = self.DATA + 'tags.txt'

        self.tag_ids = []
        self.tag_names = []

    def prepare_tags(self):
        tag_ids = []
        tag_names = []

        with open(self.TAGS_FILE, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            headers = reader.next()
            count = 0

            for row in reader:
                tag_ids.append(count)
                tag_names.append(row[headers.index("name")])
                count = count + 1

        self.tag_ids = tag_ids
        self.tag_names = tag_names


    def get_tag_name(self, tag_ref):
        return self.tag_names[tag_ref]


if __name__ == '__main__':
    tags = Tags()
    tags.prepare_tags()
