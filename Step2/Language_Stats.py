##### Language_Stats.py #####
from Process_Data import Process_Data
from Step2.Research_Stats import Research_Stats


class Language_Stats(Research_Stats):

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

    def selective_update(self, key, repo_data, byte_size, current_ordering, lang_combos):
        self.language_combos[key] = Process_Data.combine_dictionaries(
            self.language_combos[key], lang_combos)
        topics_dict = Process_Data.create_dictionary(repo_data.topics_list, [1] * repo_data.topics_used)
        self.topics[key] = Process_Data.combine_dictionaries(
            self.topics[key],
            topics_dict)
        self.times_used[key] += 1
        self.ordering[key].append(current_ordering)
        self.bytes_written[key].append(byte_size)
        self.byte_distribution[key].append(byte_size / repo_data.byte_size)
        self.languages_used[key].append(repo_data.languages_used)
        self.topics_used[key].append(repo_data.topics_used)

    def update(self, repo_data):
        # Amount of bytes written in this language in the current repository instance
        byte_size = repo_data.language_dictionary[self.language_name]
        # Dictionary of language combos that include this language in the key with all values set to 1
        lang_combos = self.create_combo_dict(repo_data.language_combinations, self.language_name)
        # List of all the keys from 'language_dict' sorted by their byte sizes (Max Value First)
        lang_byte_order = Process_Data.sort_dictionary_into_list(repo_data.language_dictionary, True)
        # Locates the Index of this language in the  list ands one for actual positioning
        current_ordering = lang_byte_order.index(self.language_name) + 1
        key = Research_Stats.AP
        self.selective_update(key, repo_data, byte_size, current_ordering, lang_combos)
        key = Research_Stats.MLP if repo_data.uses_multiple_languages else Research_Stats.SLP
        self.selective_update(key, repo_data, byte_size, current_ordering, lang_combos)

    def create_combo_dict(self, combo_list, filter_key):
        filtered_combos = list(filter(lambda x: filter_key in x and x != [filter_key], combo_list))
        sorted_combos = [sorted(x) for x in filtered_combos]
        list_of_strings = [' '.join(x) for x in sorted_combos]
        combo_dict = Process_Data.create_dictionary(list_of_strings, [1] * len(list_of_strings))
        return combo_dict

    def create_row(self, key):
        # "Language Name"
        values = [self.language_name]

        # "Occurrences"
        data = self.times_used[key]
        values.append(data)

        # "Most Frequent Language Combination"
        data = Process_Data.calculate_top_dict_key(self.language_combos[key], None)
        values.append(data)

        # "Most Frequent Topic"
        data = Process_Data.calculate_top_dict_key(self.topics[key], self.language_name.lower())
        values.append(data)

        # "Primary Language Occurrences"
        data = self.ordering[key].count(1)
        values.append(data)

        # "Language Ranking Statistics"
        data = Process_Data.calculate_stats(self.ordering[key])
        values.append(data)

        # "Bytes Written Statistics"
        data = Process_Data.calculate_stats(self.bytes_written[key])
        values.append(data)

        # "Byte Distribution Statistics"
        data = Process_Data.calculate_stats(self.byte_distribution[key])
        values.append(data)

        # "Languages Used Statistics"
        data = Process_Data.calculate_stats(self.languages_used[key])
        values.append(data)

        # "Topics Used Statistics"
        data = Process_Data.calculate_stats(self.topics_used[key])
        values.append(data)

        return values