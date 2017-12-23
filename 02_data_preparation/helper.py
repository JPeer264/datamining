import urllib
import json
import csv
import os

LASTFM_API_KEY = "8aa5abf299b1aaf6e4758f6ce3dc2fcf"
LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"


def read_csv(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        headers = reader.next()

        for row in reader:
            item = row[0]
            data.append(item)

    return data
# /read_csv


def api_call(apiString):
    """
    triggers an api to the user api
    :param method: the method of the user api, e.g. gettopartists
    :param username: the data from this user
    :return: returns a json decoded object
    """
    # urllib.quote = Replace special characters in string
    url = LASTFM_API_URL + \
        "?format=json" + \
        "&api_key=" + LASTFM_API_KEY + \
        "&" + apiString

    # Perform API-call and save (comes as String formatted as JSON)
    json_string = urllib.urlopen(url).read()

    # load() loads JSON from a file or file-like object
    # loads() loads JSON from a given string or unicode object
    return json.loads(json_string)
# /lfm_api_user_call


def save_json(objects, filepath):
    content = json.dumps(objects, indent=4, sort_keys=True)
    json_file = open(filepath, 'w')

    json_file.write(content)
    json_file.close()
# /save_json


def get_unique_items(iterable):
    """
    Deletes duplicates in array
    https://stackoverflow.com/questions/32664180/why-does-removing-duplicates-from-a-list-produce-none-none-output
    :param iterable: an array to remove duplicates
    :return: an array with no duplicates
    """
    seen = set()
    result = []

    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result
# /get_unique_items


def log_highlight(text):
    """
    #################
    ## Highlightes ## any given text and print it
    #################
    :param text:
    """
    hashes = ""

    for i in text:
        hashes += "#"

    print("")
    print("###" + hashes + "###")
    print("## " + text + " ##")
    print("###" + hashes + "###")
    print("")

    return
# /log_highlight


def ensure_dir(directory):
    """
    Ensures that the directory exists. If the directory structure does not exist, it is created.
    :param directory: any path as string
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
# /ensure_dir
