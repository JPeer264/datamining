from glob import glob
import numpy as np
import json

import helper

FETCHED_DATA = "./fetched_data/"
SAVE_DIR = "./data/"
FILENAME = "users.txt"

def prepare_users():
  dirs = np.array(glob(FETCHED_DATA + "/user_recent_tracks/*/"))

  getUsername = lambda t: t.split("/")[-2]
  all_users = np.vectorize(getUsername)

  helper.ensure_dir(SAVE_DIR)

  file = open(SAVE_DIR + FILENAME, "w")

  for user in all_users(dirs):
    file.write(user)

  file.close()
