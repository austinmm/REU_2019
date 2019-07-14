##### Process_Data.py #####

# Converts a dictionary into a class (tuple)
from collections import namedtuple  # namedtuple()
import numpy as np  # percentile()
# Checks if a path to file exist
from pathlib import Path
# Communicate with linux terminal
import subprocess
# Safely converts strings into the correct python object
import ast  # literal_eval()
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
# Allows code to read in large CSV files
csv.field_size_limit(sys.maxsize)
# Used to convert Language Codes to Language names
language_identifier = googletrans.LANGUAGES
# lemmatization words using the NLTK library
lemmatizer = WordNetLemmatizer()


class Process_Data:

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
    # This function reads in all the rows of a csv file and prepares them for processing
    def read_in_data(file_path, file_name, class_name):
        file_name = file_path + file_name + '.csv'
        file_path = Path(file_name)
        list_of_objects = []
        if file_path.is_file() == False:
            error = "No such file or directory: '" + file_name + "'"
            sys.exit(error)
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
                    for index in range(0, len(row), 1):
                        field = row[index].replace(" ", "_")
                        # key is index of the column and value is the column name
                        tuple_format[index] = field  # i.e. {1: 'name', 2: 'id'}
                    continue
                # Formats the row's fields into their correct type
                for index in range(0, len(row), 1):
                    row[index] = Process_Data.jsonString_to_object(row[index])
                # This line converts the row into an python objects
                new_object = namedtuple(class_name, tuple_format.values())(*row)
                list_of_objects.append(new_object)
        return list_of_objects

    @staticmethod
    def percentile_partition_dictionary(dictionary, upper_percent, lower_percent):
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
    def clean_text_for_nlp(text, join_text=False):
        words = nltk.word_tokenize(text)
        # Removes all punctuation, special characters and digits from text
        # str.isalnum(): Return True if all characters in 'word' are alphanumeric
        words = [word for word in words if word.isalnum()]
        # Removes all stop words from text
        words = [word for word in words if word not in stopwords.words('english')]
        '''
            Lemmatization usually refers to doing things properly with 
            the use of a vocabulary and morphological analysis of words, 
            normally aiming to remove inflectional endings only and
            to return the base or dictionary form of a word, which is known as the lemma
            * pos is the part of speech i want to convert the word to, 'n' = noun
        '''
        words = [lemmatizer.lemmatize(word) for word in words]
        if join_text:
            words = ' '.join(words)
        return words

    @staticmethod
    def translate_text(text, dest_language="en"):
        # Used to translate using the googletrans library
        import json
        translator = googletrans.Translator()
        try:
            translation = translator.translate(text=text, dest=dest_language)
            translation.src = language_identifier[translation.src]
        except json.decoder.JSONDecodeError:
            # api call restriction
            process = subprocess.Popen(["nordvpn", "d"], stdout=subprocess.PIPE)
            process.wait()
            process = subprocess.Popen(["nordvpn", "c", "Europe"], stdout=subprocess.PIPE)
            process.wait()
            return Process_Data.translate_text(text=text, dest_language=dest_language)
        return translation

    @staticmethod
    def remove_emojis(text):
        #import emoji
        #text = emoji.get_emoji_regexp().sub(u'', text)
        import re
        emoji_pattern = re.compile("["
           u"\U0001F600-\U0001F64F"  # emoticons
           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
           u"\U0001F680-\U0001F6FF"  # transport & map symbols
           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
           u"\U0001F1F2-\U0001F1F4"  # Macau flag
           u"\U0001F1E6-\U0001F1FF"  # flags
           u"\U0001F600-\U0001F64F"
           u"\U00002702-\U000027B0"
           u"\U000024C2-\U0001F251"
           u"\U0001f926-\U0001f937"
           u"\U0001F1F2"
           u"\U0001F1F4"
           u"\U0001F620"
           u"\u200d"
           u"\u2640-\u2642"
           "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
