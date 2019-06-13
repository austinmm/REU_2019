import csv
from collections import namedtuple  # Used to convert a dictionary to a python object
import json # Used to convert json string in language field of csv to python dictionary object
import ast # Used to reformat json string to be properly loaded into python dictionary object
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt; plt.rcdefaults()
import plotly.offline as pyo

def read_in_rows(file):
    repos = []
    with open(file + '.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        isHeader = True
        header_dict = {}
        for row in reader:
            if isHeader:
                for index in range(0, len(row), 1):
                    field = row[index]
                    header_dict[index] = field # i.e. -> 1: 'name', 2: 'id'
                isHeader = False
                continue
            # Converts each dictionary into a class object type
            new_repo = namedtuple("Repository", header_dict.values())(*row)
            repos.append(new_repo)
    csvFile.close()
    return repos


def answer_RQ1(list_of_repos):
    language_dict = {}
    for repo in list_of_repos:
        lang = ast.literal_eval(repo.language)
        lang = json.dumps(lang)
        languages = json.loads(lang) # i.e. languages = {'C': 123, 'Assembly': 25, ...}
        for lang, size in languages.items():
            if lang in language_dict:
                language_dict[lang] += size
            else:
                language_dict[lang] = size
    return language_dict


def answer_RQ2(list_of_repos, topics_to_ignore):
    topics_dict = {}
    for repo in list_of_repos:
        repo_topics = list(ast.literal_eval(repo.topics))
        for topic in repo_topics:
            val = topics_dict.get(topic, -1)
            if topic.lower() in topics_to_ignore:
                print("Ignoring Topic: %s" % topic)
            elif val != -1:
                print("%s: %d" % (topic, val))
                topics_dict[topic] += 1
            else:
                topics_dict[topic] = 1
    return topics_dict


def display_results(dict_data, upper_percent, lower_percent, data_set_name, file):
    results = {}
    values = np.array([float(x) for x in dict_data.values()])
    upper_limit = np.percentile(values, upper_percent, interpolation='higher')
    lower_limit = np.percentile(values, lower_percent, interpolation='lower')
    for key, value in dict_data.items():
        if upper_limit >= value >= lower_limit:
            results[key] = value
    title = str(upper_percent) + "th to " + str(lower_percent) + "th Percentile of " + data_set_name + " Used on Github"
    create_advanced_pie_graph(title, results, file)
    #create_basic_pie_graph(results.keys(), results.values())


def create_basic_pie_graph(labels, values):
    patches, texts = plt.pie(values, labels=labels, startangle=90)# autopct='%.1f%%',
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.show()


def create_advanced_pie_graph(title, dict_data, file):
    #https://plot.ly/python/pie-charts/
    slices_count = str(len(dict_data)) + " Results within Percentile"
    data = {"values": list(dict_data.values()), "labels": list(dict_data.keys()),
             "textinfo": "percent", "hoverinfo": "label+value", "hole": .5, "type": "pie"}
    fig = {
        "data": [data],
        "layout": {
            "title": title,
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": slices_count,
                    "x": 0.5,
                    "y": 0.5
                }
            ]
        }
    }
    pyo.offline.plot(fig, filename= file + '.html')


# Start Point of Program
if __name__ == '__main__':
    list_of_repos = read_in_rows("Revised_Repos")#Github_Repos, Revised_Repos
    print("Repositories Processed: %d" % len(list_of_repos))
    language_dict = answer_RQ1(list_of_repos)
    upper_percentile = 100
    lower_percentile = 85
    title = 'Programming Languages'
    file = "RQ1"
    display_results(language_dict, upper_percentile, lower_percentile, title, file)

    topics_to_ignore = [x.lower() for x in language_dict.keys()]
    topics_dict = answer_RQ2(list_of_repos, topics_to_ignore)
    upper_percentile = 100
    lower_percentile = 99
    title = 'Project Topics'
    file = "RQ2"
    display_results(topics_dict, upper_percentile, lower_percentile, title, file)
