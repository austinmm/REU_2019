import csv  # Used to read and write to csv files
from collections import namedtuple
import ast  # Used to reformat json string to be properly loaded into python dictionary object
import statistics
import copy
from collections import Counter
from itertools import chain, combinations
import abc
import json


class Research_Stats(metaclass=abc.ABCMeta):
    AP  = "All"
    SLP = "Single-Language"
    MLP = "Multi-Language"
    Project_Types = [AP, SLP, MLP]

    def __init__(self):
        self.list_of_repos = []
        self.repositories_stats = []
        self.repo_count = 0

    @staticmethod
    def create_dictionary(keys, values):
        return {k: v for (k, v) in zip(keys, values)}

    @staticmethod
    def combine_dictionaries(dict1, dict2):
        return dict(Counter(dict1) + Counter(dict2))

    @staticmethod
    def sort_dictionary_into_list(dictionary, sortByMaxValue):
        return list(sorted(dictionary, key=dictionary.__getitem__, reverse=sortByMaxValue))

    @staticmethod
    def sort_list(array, sortByMaxValue):
        return list(sorted(array, reverse=sortByMaxValue))

    @staticmethod
    def jsonString_to_object(json_string):
        value = ''
        try:
            value = ast.literal_eval(json_string)
        except SyntaxError:
            value = json_string
        except ValueError:
            value = json_string
        return value

    @staticmethod
    def calculate_top_dict_key(dictionary, exclude_key):
        deep_copy = copy.deepcopy(dictionary)
        if (exclude_key != None) and (exclude_key in deep_copy):
            deep_copy.pop(exclude_key)
        max_key = ''
        if len(deep_copy) != 0:
            max_key = max(deep_copy, key=deep_copy.get)
        return max_key

    @staticmethod
    def calculate_stats(array):
        stat_dict = {'sum': 0, 'avg': 0, 'std': 0, 'var': 0}
        stat_dict['sum'] = sum(array)
        if len(array) >= 2:
            stat_dict['avg'] = round(statistics.mean(array), 2)
            stat_dict['std'] = round(statistics.stdev(array), 2)
            stat_dict['var'] = round(statistics.variance(array), 2)
        return str(stat_dict)

    # This function reads in all the rows of a csv file and prepares them for processing
    def read_in_data(self, file_path, file_name, class_name):
        list_of_objects = []
        # Opens the CSV file for reading
        file_name = file_path + file_name + '.csv'
        with open(file_name, 'r') as csv_file:
            reader = csv.reader(csv_file)
            is_header_row = True
            tuple_format = {}
            # Every row is a unique repository
            for row in reader:
                # The first row of the CSV file contains all the column names/headers
                if is_header_row:
                    is_header_row = False # We only want to execute this conditional once
                    # Creates the field names for our python object from csv header row fields
                    for index in range(0, len(row), 1):
                        field = row[index].replace(" ", "_")
                        # key is index of the column and value is the column name
                        tuple_format[index] = field  # i.e. {1: 'name', 2: 'id'}
                    continue
                # Formats the row's fields into their correct type
                for index in range(0, len(row), 1):
                    row[index] = Research_Stats.jsonString_to_object(row[index])
                # This line converts the row into an python objects
                new_object = namedtuple(class_name, tuple_format.values())(*row)
                list_of_objects.append(new_object)
        return list_of_objects

    @abc.abstractmethod
    def write_data(self, file_path):
        pass

    def process_repository_data(self, file_path, file_name):
        self.list_of_repos = self.read_in_data(file_path, file_name, "Repository")
        self.repo_count = len(self.list_of_repos)
        print("Repositories Processed: %d" % self.repo_count)
        index = 1
        for repo in self.list_of_repos:
            current_repository = Repository_Stats(repo)
            self.repositories_stats.append(current_repository)
            self.update_statistics(current_repository)
            print("Repository %d: Percentage Complete: %.2f" % (index, (index / self.repo_count * 100)))
            index += 1
        self.write_data(file_path)

    @abc.abstractmethod
    def update_statistics(self, current_repository):
        pass


class RQ1_Stats(Research_Stats):

    def __init__(self):
        super(RQ1_Stats, self).__init__()
        self.languages_stats = {}

    def update_statistics(self, current_repository):
        for language in current_repository.language_dict:
            if language not in self.languages_stats:
                self.languages_stats[language] = Language_Stats(language)
            self.languages_stats[language].update(current_repository)

    def write_data(self, file_path):
        # Creates/Overwrites a csv file to write to
        self.write_repo_data(file_path)
        self.write_lang_data(file_path)

    def write_repo_data(self, file_path):
        # Creates/Overwrites a csv file to write to
        print("Writing Repository Data to CSV File...")
        file_name = file_path + 'RQ1_Repositories.csv'
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            # Writes the dictionary keys to the csv file
            writer.writerow(Repository_Stats.Header_Names)
            # Writes all the values of each index of dict_repos as separate rows in the csv file
            for repo in self.repositories_stats:
                # If the repo is not a multi-language project then we ignore it
                row = repo.create_row()
                writer.writerow(row)
        csv_file.close()
        print("Finished Writing Repository Data to '%s.csv'" % file_name)

    def write_lang_data(self, file_path):
        # Creates/Overwrites a csv file to write to
        print("Writing Language Data to CSV Files...")
        for projectType in Research_Stats.Project_Types:
            file_name = file_path + 'RQ1_' + projectType + '.csv'
            with open(file_name, 'w') as csv_file:
                writer = csv.writer(csv_file)
                # Writes the dictionary keys to the csv file
                writer.writerow(Language_Stats.Header_Names)
                # Writes all the values of each index of dict_repos as separate rows in the csv file
                for language, lang_object in self.languages_stats.items():
                    # If the repo is not a multi-language project then we ignore it
                    row = lang_object.create_row(projectType)
                    writer.writerow(row)
            csv_file.close()
            print("Finished Writing Language Data to '%s.csv'" % file_name)

    def process_language_data(self, file_path, file_name):
        values = self.read_in_data(file_path, file_name, "Language")
        keys = [x.Language_Name for x in values]
        self.languages_stats = Research_Stats.create_dictionary(keys, values)

    # Byte Distribution Statistics
    def byte_distribution_stats(self, stat_key):
        if stat_key is not None:
            return {key: value.Byte_Distribution_Statistics[stat_key] for key, value in self.languages_stats.items()}
        return {key: value.Byte_Distribution_Statistics for key, value in self.languages_stats.items()}

    # Bytes Written Statistics
    def bytes_written_stats(self, stat_key):
        if stat_key is not None:
            return {key: value.Bytes_Written_Statistics[stat_key] for key, value in self.languages_stats.items()}
        return {key: value.Bytes_Written_Statistics for key, value in self.languages_stats.items()}

    # Occurrences
    def occurrence_counts(self):
        return {key: value.Occurrences for key, value in self.languages_stats.items()}

    # Most Frequent Language Combination
    def language_combinations(self):
        return {key: value.Most_Frequent_Language_Combination for key, value in self.languages_stats.items()}

    # Most Frequent Topic
    def topic_frequencies(self):
        return {key: value.Most_Frequent_Topic for key, value in self.languages_stats.items()}

    # Primary Language Occurrences
    def primary_language_counts(self):
        return {key: value.Primary_Language_Occurrences for key, value in self.languages_stats.items()}

    # Language Ranking Statistics
    def ranking_stats(self, stat_key):
        if stat_key is not None:
            return {key: value.Language_Ranking_Statistics[stat_key] for key, value in self.languages_stats.items()}
        return {key: value.Language_Ranking_Statistics for key, value in self.languages_stats.items()}

    # Languages Used Statistics
    def languages_used_stats(self, stat_key):
        if stat_key is not None:
            return {key: value.Languages_Used_Statistics[stat_key] for key, value in self.languages_stats.items()}
        return {key: value.Languages_Used_Statistics for key, value in self.languages_stats.items()}

    # Topics Used Statistics
    def topics_used_stats(self, stat_key):
        if stat_key is not None:
            return {key: value.Topics_Used_Statistics[stat_key] for key, value in self.languages_stats.items()}
        return {key: value.Topics_Used_Statistics for key, value in self.languages_stats.items()}


class Language_Stats:

    Header_Names = ["Language Name", "Occurrences", "Most Frequent Language Combination",
                    "Most Frequent Topic", "Primary Language Occurrences", "Language Ranking Statistics",
                    "Bytes Written Statistics", "Byte Distribution Statistics",
                    "Languages Used Statistics", "Topics Used Statistics"]

    def __init__(self, language):
        self.language_name = language
        # self.language_combos: Contains all language combinations (key) with their occurrence count (value)
        self.language_combos = {Research_Stats.AP: {}, Research_Stats.SLP: {}, Research_Stats.MLP: {}}
        # self.topics: Dictionary of all topics that existed
        self.topics = {Research_Stats.AP: {}, Research_Stats.SLP: {}, Research_Stats.MLP: {}}
        # self.times_used: Integer count of the amount of times this language was used
        self.times_used = {Research_Stats.AP: 0, Research_Stats.SLP: 0, Research_Stats.MLP: 0}
        # self.bytes_written: Integer count of the amount of bytes written in this language
        self.bytes_written = {Research_Stats.AP: [], Research_Stats.SLP: [], Research_Stats.MLP: []}
        # self.ordering: List of integers representing the order/position, based off of bytes, this language appeared in
        self.ordering = {Research_Stats.AP: [], Research_Stats.SLP: [], Research_Stats.MLP: []}
        # self.languages_used: List of integers representing the amount of languages used in tandem with this language
        self.languages_used = {Research_Stats.AP: [], Research_Stats.SLP: [], Research_Stats.MLP: []}
        # self.topics_used: List of integers representing the amount of topics used when this language is present
        self.topics_used = {Research_Stats.AP: [], Research_Stats.SLP: [], Research_Stats.MLP: []}
        # self.byte_distribution: List of percentage of bytes written out of all bytes in repo in this language
        self.byte_distribution = {Research_Stats.AP: [], Research_Stats.SLP: [], Research_Stats.MLP: []}

    def update_data(self, key, repo_data, byte_size, current_ordering, lang_combos):
        self.language_combos[key] = Research_Stats.combine_dictionaries(
            self.language_combos[key], lang_combos)
        self.topics[key] = Research_Stats.combine_dictionaries(
            self.topics[key],
            repo_data.topics_dict)
        self.times_used[key] += 1
        self.ordering[key].append(current_ordering)
        self.bytes_written[key].append(byte_size)
        self.byte_distribution[key].append(byte_size / repo_data.byte_size)
        self.languages_used[key].append(repo_data.languages_used)
        self.topics_used[key].append(repo_data.topics_used)

    def update(self, repo_data):
        # Amount of bytes written in this language in the current repository instance
        byte_size = repo_data.language_dict[self.language_name]
        # Dictionary of language combos that include this language in the key with all values set to 1
        lang_combos = self.create_combo_dict(repo_data.language_combinations, self.language_name)
        # List of all the keys from 'language_dict' sorted by their byte sizes (Max Value First)
        lang_byte_order = Research_Stats.sort_dictionary_into_list(repo_data.language_dict, True)
        # Locates the Index of this language in the  list ands one for actual positioning
        current_ordering = lang_byte_order.index(self.language_name) + 1
        key = Research_Stats.AP
        self.update_data(key, repo_data, byte_size, current_ordering, lang_combos)
        key = Research_Stats.MLP if repo_data.isMultiLanguage else Research_Stats.SLP
        self.update_data(key, repo_data, byte_size, current_ordering, lang_combos)

    def create_combo_dict(self, combo_list, filter_key):
        filtered_combos = list(filter(lambda x: filter_key in x and x != [filter_key], combo_list))
        sorted_combos = [sorted(x) for x in filtered_combos]
        list_of_strings = [' '.join(x) for x in sorted_combos]
        combo_dict = Research_Stats.create_dictionary(list_of_strings, [1] * len(list_of_strings))
        return combo_dict

    def create_row(self, key):
        # "Language Name"
        values = [self.language_name]

        # "Occurrences"
        data = self.times_used[key]
        values.append(data)

        # "Most Frequent Language Combination"
        data = Research_Stats.calculate_top_dict_key(self.language_combos[key], None)
        values.append(data)

        # "Most Frequent Topic"
        data = Research_Stats.calculate_top_dict_key(self.topics[key], self.language_name.lower())
        values.append(data)

        # "Primary Language Occurrences"
        data = self.ordering[key].count(1)
        values.append(data)

        # "Language Ranking Statistics"
        data = Research_Stats.calculate_stats(self.ordering[key])
        values.append(data)

        # "Bytes Written Statistics"
        data = Research_Stats.calculate_stats(self.bytes_written[key])
        values.append(data)

        # "Byte Distribution Statistics"
        data = Research_Stats.calculate_stats(self.byte_distribution[key])
        values.append(data)

        # "Languages Used Statistics"
        data = Research_Stats.calculate_stats(self.languages_used[key])
        values.append(data)

        # "Topics Used Statistics"
        data = Research_Stats.calculate_stats(self.topics_used[key])
        values.append(data)

        return values


class Repository_Stats:

    Header_Names = ["Score", "Multi-Language", "Languages Used", "Main Language",
                    "All Languages", "Language Combinations", "Topics Used", "Topics",
                    "Description", "Description NLP", "Owner Type", "Open Issues"
                    "Stars", "Watchers", "Forks"]

    def __init__(self, repo):
        # Dictionary of languages as keys with values the amount of bytes written in said language
        self.language_dict = repo.language
        # Amount of bytes written in this language in the current repository instance
        self.byte_size = sum(list(self.language_dict.values()))
        # String value of the primary language, in bytes written, of the current repo
        self.main_language = Research_Stats.calculate_top_dict_key(self.language_dict, None)
        # Amount of languages used in current repository instance
        self.languages_used = len(self.language_dict)
        # Dictionary of language combos that include this language in the key with all values set to 1
        self.language_combinations = self.create_unique_combo_list(self.language_dict, self.languages_used)
        # Boolean that represents if this repository uses multiple languages or not
        self.isMultiLanguage = True if self.languages_used > 1 else False
        # List of topics used in current repository instance
        self.topics_list = repo.topics
        # Amount of topics used in current repository instance
        self.topics_used = len(self.topics_list)
        # Dictionary of topics as keys with all values set to 1
        self.topics_dict = Research_Stats.create_dictionary(self.topics_list, [1] * self.topics_used)
        self.description = repo.description
        self.nlp_description = ''
        self.owner_type = repo.owner['type']
        self.open_issues = repo.open_issues
        self.stars = repo.stargazers_count
        self.watchers = repo.subscribers_count
        self.forks = repo.forks
        self.score = repo.score

    def create_row(self):
        # "Score"
        values = [self.score]

        # "Multi-Language"
        data = self.isMultiLanguage
        values.append(data)

        # "Languages Used"
        data = self.languages_used
        values.append(data)

        # "Main Language"
        data = self.main_language
        values.append(data)

        # "All Languages"
        data = list(self.language_dict.keys())
        values.append(data)

        # "Language Combinations"
        data = self.language_combinations
        values.append(data)

        # "Topics Used"
        data = self.topics_used
        values.append(data)

        # "Topics"
        data = self.topics_list
        values.append(data)

        # "Description"
        data = self.description
        values.append(data)

        # "Description NLP"
        data = self.nlp_description
        values.append(data)

        # "Owner Type"
        data = self.owner_type
        values.append(data)

        # "Open Issues"
        data = self.open_issues
        values.append(data)

        # "Stars"
        data = self.stars
        values.append(data)

        # "Watchers"
        data = self.watchers
        values.append(data)

        # "Forks"
        data = self.forks
        values.append(data)

        return values

    def create_unique_combo_list(self, dictionary, dict_count):
        combos = []
        if dict_count > 5:
            print("This repo uses %d languages; however, the combo limit is 20 languages" % dict_count)
            return combos
        items = list(dictionary.keys())
        for i in range(2, dict_count + 1, 1):
            sub_combo = [list(x) for x in combinations(items, i)]
            if len(sub_combo) > 0:
                combos.extend(sub_combo)
        return combos

    def _create_unique_combo_list(self,  dictionary, dict_count):
        combos = []
        if dict_count > 20:
            print("This repo uses %d languages; however, the combo limit is 20 languages" % dict_count)
            #return combos
        items = list(dictionary.keys())
        combos = list(chain(*map(lambda x: combinations(items, x), range(2, dict_count + 1))))
        return combos

    def __create_unique_combo_list(self, dictionary, dict_count):
        combo = []
        if dict_count > 20:
            print("This repo uses %d languages; however, the combo limit is 20 languages" % dict_count)
            #return combos
        items = list(dictionary)  # allows duplicate elements
        combo = list(chain.from_iterable(combinations(items, r) for r in range(2, dict_count + 1)))
        return combo

# Start Point of Program
research_data = RQ1_Stats()
file_path = ""   # "/content/drive/My Drive/Austin Marino/Colab App/"
file_name = "Revised_Repos"
research_data.process_repository_data(file_path, file_name)
'''
file_name = "RQ1_All"
research_data.process_language_data(file_path, file_name)
vals = research_data.byte_distribution_stats(None)
vals = research_data.languages_used_stats('avg')
print("There are a total of %d unique programing languages" % research_data.repo_count)
'''