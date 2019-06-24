import csv  # Used to read and write to csv files
from collections import namedtuple
import ast  # Used to reformat json string to be properly loaded into python dictionary object
import statistics
import copy
from collections import Counter
from itertools import combinations

class Research_Stats:
    AP  = "All"
    SLP = "Single-Language"
    MLP = "Multi-Language"
    Project_Types = [AP, SLP, MLP]

    def __init__(self):
        self.repo_keys = []
        self.list_of_repos = []
        self.repositories_stats = []
        self.languages_stats = {}
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
        return ast.literal_eval(json_string)

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

    # This function reads in all the rows, repo dictionary objects, from the csv file
    def read_in_rows(self, file_name):
        # Opens the CSV file for reading
        with open(file_name + '.csv', 'r') as csv_file:  # "/content/drive/My Drive/Austin Marino/Colab App/" +
            reader = csv.reader(csv_file)
            is_header_row = True
            headers = {}
            tuple_format = {}
            # Every row is a unique repository
            for row in reader:
                # The first row of the CSV file contains all the column names/headers
                if is_header_row:
                    is_header_row = False # We only want to execute this conditional once
                    # Creates the field names for our python object from csv header row fields
                    self.repo_keys = row
                    for index in range(0, len(row), 1):
                        field = row[index]
                        # key is index of the column and value is the column name
                        tuple_format[index] = field  # i.e. {1: 'name', 2: 'id'}
                        # vice-versa
                        headers[field] = index  # i.e. {'name': 1, 'id': 2}
                    continue
                # These lines convert dictionaries and list strings into actual python versions
                row[headers['language']] = Research_Stats.jsonString_to_object(row[headers['language']])
                row[headers['topics']] = Research_Stats.jsonString_to_object(row[headers['topics']])
                row[headers['owner']] = Research_Stats.jsonString_to_object(row[headers['owner']])
                # This line converts all the repository rows into python objects under the class name "Repository"
                repo_object = namedtuple("Repository", tuple_format.values())(*row)
                self.list_of_repos.append(repo_object)
        self.repo_count = len(self.list_of_repos)
        print("Repositories Processed: %d" % self.repo_count)

    def write_to_csv(self):
        # Creates/Overwrites a csv file to write to
        print("Writing Research Data to CSV Files...")
        self.write_language_data()

    def write_language_data(self):
        # Creates/Overwrites a csv file to write to
        print("Writing Language Data to CSV Files...")
        for projectType in Research_Stats.Project_Types:
            file_name = 'RQ1_' + projectType + '.csv'
            with open(file_name, 'w') as csv_file:
                writer = csv.writer(csv_file)
                # Writes the dictionary keys to the csv file
                writer.writerow(Language_Stats.Header_Names)
                # Writes all the values of each index of dict_repos as separate rows in the csv file
                for language, lang_object in self.languages_stats.items():
                    # If the repo is not a multi-language project then we ignore it
                    writer.writerow(lang_object.create_row(projectType))
            csv_file.close()
            print("Finished Writing Repositories to '%s.csv'" % file_name)

    def process_repository_data(self):
        index = 1
        for repo in self.list_of_repos:
            current_repository = Repository_Stats(repo)
            self.repositories_stats.append(current_repository)
            self.update_language_statistics(current_repository)
            print("Repository %d: Percentage Complete: %.2f" % (index, (index / self.repo_count * 100)))
            index += 1

    def update_language_statistics(self, current_repository):
        for language in current_repository.language_dict:
            if language not in self.languages_stats:
                self.languages_stats[language] = Language_Stats(language)
            self.languages_stats[language].update(current_repository)


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

    def single_language_update(self, repo_data, byte_size):
        self.topics[Research_Stats.SLP] = Research_Stats.combine_dictionaries(
            self.topics[Research_Stats.SLP],
            repo_data.topics_dict)
        self.times_used[Research_Stats.SLP] += 1
        self.bytes_written[Research_Stats.SLP].append(byte_size)
        self.topics_used[Research_Stats.SLP].append(repo_data.topics_used)
        self.ordering[Research_Stats.SLP].append(1)
        self.languages_used[Research_Stats.SLP].append(1)
        self.byte_distribution[Research_Stats.SLP].append(byte_size / repo_data.byte_size)

    def multi_language_update(self, repo_data, byte_size, current_ordering):
        self.language_combos[Research_Stats.MLP] = self.language_combos[Research_Stats.AP]
        self.topics[Research_Stats.MLP] = Research_Stats.combine_dictionaries(
            self.topics[Research_Stats.MLP],
            repo_data.topics_dict)
        self.times_used[Research_Stats.MLP] += 1
        self.bytes_written[Research_Stats.MLP].append(byte_size)
        self.ordering[Research_Stats.MLP].append(current_ordering)
        self.languages_used[Research_Stats.MLP].append(repo_data.languages_used)
        self.topics_used[Research_Stats.MLP].append(repo_data.topics_used)
        self.byte_distribution[Research_Stats.MLP].append(byte_size / repo_data.byte_size)

    def update(self, repo_data):
        # Amount of bytes written in this language in the current repository instance
        byte_size = repo_data.language_dict[self.language_name]
        # Dictionary of language combos that include this language in the key with all values set to 1
        lang_combos = self.create_combo_dict(repo_data.language_combinations, self.language_name)
        # Enters Values into Dictionaries under the key "All" (ALL Projects)
        self.language_combos[Research_Stats.AP] = Research_Stats.combine_dictionaries(self.language_combos[Research_Stats.AP], lang_combos)
        self.topics[Research_Stats.AP] = Research_Stats.combine_dictionaries(self.topics[Research_Stats.AP], repo_data.topics_dict)
        self.times_used[Research_Stats.AP] += 1
        self.bytes_written[Research_Stats.AP].append(byte_size)
        # List of all the keys from 'language_dict' sorted by their byte sizes (Max Value First)
        lang_byte_order = Research_Stats.sort_dictionary_into_list(repo_data.language_dict, True)
        # Locates the Index of this language in the  list ands one for actual positioning
        current_ordering = lang_byte_order.index(self.language_name) + 1
        self.ordering[Research_Stats.AP].append(current_ordering)
        self.languages_used[Research_Stats.AP].append(repo_data.languages_used)
        self.topics_used[Research_Stats.AP].append(repo_data.topics_used)
        self.byte_distribution[Research_Stats.AP].append(byte_size / repo_data.byte_size)
        if repo_data.isMultiLanguage:
            self.multi_language_update(repo_data, byte_size, current_ordering)
        else:
            self.single_language_update(repo_data, byte_size)

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

    def __init__(self, repo):
        # Dictionary of languages as keys with values the amount of bytes written in said language
        self.language_dict = repo.language
        # Amount of bytes written in this language in the current repository instance
        self.byte_size = sum(list(self.language_dict.values()))
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
        self.topic_combinations = []
        self.owner_type = repo.owner['type']
        self.open_issues = int(repo.open_issues)
        self.stars = int(repo.stargazers_count)
        self.watchers = int(repo.subscribers_count)

    def create_unique_combo_list(self, dictionary, dict_count):
        combos = []
        if dict_count > 5:
            print("This repo uses %d languages; however, the combo limit is 20 languages" % dict_count)
            return combos
        languages = list(dictionary.keys())
        for i in range(0, dict_count + 1, 1):
            sub_combo = [list(x) for x in combinations(languages, i)]
            if len(sub_combo) > 0:
                combos.extend(sub_combo)
        combos.remove([])
        return combos


# Start Point of Program
research_data = Research_Stats()
research_data.read_in_rows("Revised_Repos")
# Creates a Language_stats object from language and topics data
research_data.process_repository_data()
research_data.write_to_csv()
print("There are a total of %d unique programing languages" % research_data.repo_count)