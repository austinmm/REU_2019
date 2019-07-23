##### Process_Data.py #####

import statistics  # mean(), stdev(), variance()
# Finds all unique combinations within a list
from itertools import combinations  # combinations()
# Combines dictionary keys and their values
from collections import Counter
# Displays a progress bar while looping through an iterable object
from progressbar import ProgressBar  # ProgressBar()
# Deep Copies a python object
import copy  # deepcopy()
# Translates strings from one natural language to another
import googletrans
# List of all stop words in the English Language
import nltk; nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Reads/Writes in a CSV formatted file
import csv  # reader()
import sys  # sys.maxsize
# Regex
import re
# Allows code to read in large CSV files
csv.field_size_limit(sys.maxsize)
# Used to convert Language Codes to Language names
language_identifier = googletrans.LANGUAGES
# lemmatization words using the NLTK library
lemmatizer = WordNetLemmatizer()


class Process_Data:
    Server_Num = 201

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
        # Safely converts strings into the correct python object
        import ast  # literal_eval()
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

    @staticmethod
    def create_unique_combo_list(dictionary, dict_count, max_combo_count, min_combo_count=1):
        combos = []
        items = list(dictionary.keys())
        if dict_count < min_combo_count or dict_count > max_combo_count:
            return combos
        for i in range(min_combo_count, dict_count + 1, 1):
            sub_combo = [list(x) for x in combinations(items, i)]
            if len(sub_combo) > 0:
                combos.extend(sub_combo)
        return combos

    @staticmethod
    def check_if_path_exist(file):
        # Checks if a path to file exist
        from pathlib import Path
        file_path = Path(file)
        if file_path.is_file() == False:
            error = "No such path to file: '" + file + "'"
            sys.exit(error)


    @staticmethod
    def named_tuple_format(key_list):
        # Creates the field names for our python object from csv header row fields
        tuple_format = {}
        for index in range(0, len(key_list), 1):
            key = key_list[index].replace(" ", "_").lower()
            # key is index of the column and value is the column name
            tuple_format[index] = key  # i.e. {1: 'name', 2: 'id'}
        return tuple_format


    @staticmethod
    # This function reads in all the rows of a csv file and prepares them for processing
    def read_in_data(file_path, file_name, class_name):
        file_name = file_path + file_name + '.csv'
        Process_Data.check_if_path_exist(file=file_name)
        list_of_objects = []
        # Opens the CSV file for reading
        with open(file_name, 'r') as csv_file:
            reader = csv.reader(csv_file)
            is_header_row = True
            tuple_format = {}
            # Every row is a unique item
            pbar = ProgressBar()
            for row in pbar(list(reader)):
                # The first row of the CSV file contains all the column names/headers
                if is_header_row:
                    is_header_row = False  # We only want to execute this conditional once
                    # Creates the field names for our python object from csv header row fields
                    tuple_format = Process_Data.named_tuple_format(row)
                    continue
                # Formats the row's fields into their correct type
                for index in range(0, len(row), 1):
                    row[index] = Process_Data.jsonString_to_object(row[index])
                # This line converts the row into an python objects
                new_object = Process_Data.convert_to_named_tuple(class_name=class_name,
                                                                 dictionary=tuple_format,
                                                                 values=row
                                                                 )
                list_of_objects.append(new_object)
        return list_of_objects

    @staticmethod
    def convert_to_named_tuple(class_name, dictionary, values):
        # Converts a dictionary into a class (tuple)
        from collections import namedtuple  # namedtuple()
        return namedtuple(class_name, dictionary.values())(*values)

    @staticmethod
    def percentile_partition_dictionary(dictionary, upper_percent, lower_percent):
        import numpy as np
        results = {}
        values = np.array([float(x) for x in dictionary.values()])
        upper_limit = np.percentile(values, upper_percent, interpolation='higher')
        lower_limit = np.percentile(values, lower_percent, interpolation='lower')
        for key, value in dictionary.items():
            if upper_limit >= value >= lower_limit:
                results[key] = value
        if len(results) > 100:
            print("Error: Too many results within percentiles specified.")
            return {}
        return results

    @staticmethod
    def process_text_for_nlp(text):
        # Word Tokenization
        words = nltk.word_tokenize(text)
        # Remove Non-alpha text
        words = [re.sub(r'[^a-z]', '', word) for word in words if word.isalnum()]
        # Removes all stop words from text and words that are less than two characters in length
        words = [word for word in words if word not in stopwords.words('english') and len(word) > 1]
        '''
            Lemmatization: removes inflectional endings only and
            to return the base or dictionary form of a word, which is known as the lemma
        '''
        # Word Lemmatization
        words = [lemmatizer.lemmatize(word) for word in words]
        return words

    @staticmethod
    def clean_text(text):
        # Change all the text to lower case
        text = text.lower()
        # Converts all '+' and '/' to the word 'and'
        text = re.sub(r'[+|/]', ' and ', text)
        # Removes all characters besides numbers, letters, and commas
        text = re.sub(r'[^\w\d,]', ' ', text)
        # Word Tokenization
        words = text.split()
        # Joins tokenized string into one string
        text = ' '.join(words)
        return text

    @staticmethod
    def translate_text(text, dest_language="en"):
        # Used to translate using the googletrans library
        translator = googletrans.Translator()
        import json; import emoji; import requests
        # Removes emojis that would cause errors during translation
        text = emoji.get_emoji_regexp().sub(r'', text)
        try:
            translation = translator.translate(text=text, dest=dest_language)
            translation.src = language_identifier[translation.src.lower()]
        except requests.exceptions.ConnectionError as e:
            Process_Data.change_ip_address()
            return Process_Data.translate_text(text=text, dest_language=dest_language)
        except json.decoder.JSONDecodeError as e:
            # api call restriction
            Process_Data.change_ip_address()
            return Process_Data.translate_text(text=text, dest_language=dest_language)
        return translation

    @staticmethod
    def change_ip_address():
        # Communicate with linux terminal
        import subprocess
        process = subprocess.Popen(["nordvpn", "d"], stdout=subprocess.PIPE)
        process.wait()
        server = "au" + str(Process_Data.Server_Num)
        Process_Data.Server_Num += 1
        process = subprocess.Popen(["nordvpn", "c", server], stdout=subprocess.PIPE)
        process.wait()

    @staticmethod
    def search_wikipedia(text):
        import wikipedia
        try:
            result = wikipedia.search(text, results=3, suggestion=False)
            return None if result is None or result == [] else result[0].lower()
        except wikipedia.exceptions.PageError:
            result = wikipedia.suggest(text)
            return None if result is None else result.lower()
        except wikipedia.exceptions.DisambiguationError as other_options:
            return Process_Data.search_wikipedia(other_options.options[0])
        except wikipedia.exceptions.HTTPTimeoutError:
            Process_Data.change_ip_address()
            return Process_Data.search_wikipedia(text)

    @staticmethod
    def store_data(file_path, file_name, data):
        # Saves objects to be loaded at a later time
        import pickle
        # Its important to use binary mode
        file = file_path + file_name
        # Opens to write binary
        pickle_file = open(file, 'wb')
        # source, destination
        pickle.dump(data, pickle_file)
        pickle_file.close()

    @staticmethod
    def load_data(file_path, file_name):
        # Saves objects to be loaded at a later time
        import pickle
        # Its important to use binary mode
        file = file_path + file_name
        # Opens to write binary
        pickle_file = open(file, 'rb')
        # source, destination
        data = pickle.load(file=pickle_file)
        pickle_file.close()
        return data
