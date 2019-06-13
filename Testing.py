import csv
from collections import namedtuple  # Used to convert a dictionary to a python object
import json # Used to convert json string in language field of csv to python dictionary object
import ast # Used to reformat json string to be properly loaded into python dictionary object
import matplotlib.pyplot as plt


# Start Point of Program
if __name__ == '__main__':
    dict1 = {"value": 5, "score": 1, "url": "www.home.com", "count": 1, "languages": "{'C': 1, 'C#': 20}"}
    dict2 = {"count": 2, "languages": "{'python': 5, 'java': 2}", "value": "5"}
    dict1.update(dict2)
    print(dict1)
    original_repo_count = 2000
    final_repo_count = 1134
    print("Valid Repositories Remaining %d of %d [%.2f%%]" % (final_repo_count, original_repo_count, (final_repo_count / original_repo_count) * 100))

