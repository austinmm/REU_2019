# Feature extraction from text
# Method: bag of words

'''
* Naive Bayes is a simple technique for constructing classifiers: models that assign class labels to problem instances,
    represented as vectors of feature values, where the class labels are drawn from some finite set.
* Method for text categorization, the problem of judging documents as belonging to one
    category or the other with word frequencies as the features.
'''

import csv
from collections import namedtuple  # Used to convert a dictionary to a python object
from sklearn.feature_extraction.text import CountVectorizer
import ast # Used to reformat json string to be properly loaded into python dictionary object
from sklearn.naive_bayes import GaussianNB
import numpy


def read_in_csv(file):
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
    return repos


def bag_of_words_method(array_of_strings):
    vectorizer = CountVectorizer()
    #The number of elements is called the dimension.
    binary_strings = vectorizer.fit_transform(array_of_strings).todense()
    print(binary_strings)
    print(vectorizer.vocabulary_)
    return binary_strings


def answer_RQ3(list_of_repos):
    pass


def prepare_repo_topics(list_of_repos):
    list_of_topic_strings = []
    for repo in list_of_repos:
        repo_topics = list(ast.literal_eval(repo.topics))
        topic_str = " ".join(repo_topics)
        print(topic_str)
        list_of_topic_strings.append(topic_str)
    return list_of_topic_strings


def get_topics_for_repos(list_of_repos):
    list_of_topics = []
    for repo in list_of_repos:
        repo_topics = list(ast.literal_eval(repo.topics))
        list_of_topics.append(repo_topics)
    return list_of_topics


def create_naive_bayes_classifier_dict(list_of_repos):
    list_of_dict = []
    for repo in list_of_repos:
        items = dict(ast.literal_eval(repo.language))
        main_lang = max(items, key=items.get)
        items.pop(main_lang)
        new_dict = {main_lang: []}
        new_dict[main_lang] = list(items.keys())
        list_of_dict.append(new_dict)
    return list_of_dict


def create_specialized_csv(list_of_repos):



if __name__ == '__main__':
    list_of_repos = read_in_csv("Revised_Repos")
    create_specialized_csv(list_of_repos, )
    print("Repositories Processed: %d" % len(list_of_repos))
    nbc_dict = create_naive_bayes_classifier_dict(list_of_repos)
    list_of_topic_strings = prepare_repo_topics(list_of_repos)
    binary_strings = bag_of_words_method(list_of_topic_strings)
    gaunb = GaussianNB()
    binary_strings = binary_strings.tolist()
    X = binary_strings  # X = [[]]
    Y = [list((x.keys()))[0] for x in nbc_dict] # Y = []
    # create dataset
    # train classifier with dataset
    print("len(X): %d\nlen(Y):%d" %(len(X), len(Y)))
    gaunb = gaunb.fit(X, Y)

    # predict using classifier
    prediction = gaunb.predict([[0,1]])
    print(prediction)


