##### Language_Stats.py #####
from Process_Data import Process_Data


class Language_Stats():

    ALP = "All-Languages"
    SLP = "Single-Languages"
    MLP = "Multiple-Languages"
    Project_Types = [ALP, SLP, MLP]

    Header_Names = ["language name", "use count", "language combinations",
                    "topics list", "primary language occurrences", "language tier statistics",
                    "bytes written statistics", "byte distribution statistics",
                    "languages used statistics", "topics used statistics"]

    def __init__(self, language):
        self.language_name = language
        # self.language_combos: Contains all language combinations (key) with their occurrence count (value)
        self.language_combinations = {Language_Stats.ALP: {}, Language_Stats.SLP: {}, Language_Stats.MLP: {}}
        # self.topics: Dictionary of all topics that existed
        self.topics_list = {Language_Stats.ALP: {}, Language_Stats.SLP: {}, Language_Stats.MLP: {}}
        # self.times_used: Integer count of the amount of times this language was used
        self.use_count = {Language_Stats.ALP: 0, Language_Stats.SLP: 0, Language_Stats.MLP: 0}
        # self.bytes_written: Integer count of the amount of bytes written in this language
        self.bytes_written = {Language_Stats.ALP: [], Language_Stats.SLP: [], Language_Stats.MLP: []}
        # self.ordering: List of integers representing the order/position, based off of bytes, this language appeared in
        self.tiers = {Language_Stats.ALP: [], Language_Stats.SLP: [], Language_Stats.MLP: []}
        # self.languages_used: List of integers representing the amount of languages used in tandem with this language
        self.languages_used = {Language_Stats.ALP: [], Language_Stats.SLP: [], Language_Stats.MLP: []}
        # self.topics_used: List of integers representing the amount of topics used when this language is present
        self.topics_used = {Language_Stats.ALP: [], Language_Stats.SLP: [], Language_Stats.MLP: []}
        # self.byte_distribution: List of percentage of bytes written out of all bytes in repo in this language
        self.byte_distribution = {Language_Stats.ALP: [], Language_Stats.SLP: [], Language_Stats.MLP: []}

    def selective_update(self, key, repo_data, byte_size, current_ordering, lang_combos):
        for combo in lang_combos:
            self.language_combinations[key][combo] = self.language_combinations[key].get(combo, 0) + 1
        for topic in repo_data.topics_list:
            self.topics_list[key][topic] = self.topics_list[key].get(topic, 0) + 1
        self.use_count[key] += 1
        self.tiers[key].append(current_ordering)
        self.bytes_written[key].append(byte_size)
        self.byte_distribution[key].append(byte_size / repo_data.total_bytes_written)
        self.languages_used[key].append(repo_data.languages_used)
        self.topics_used[key].append(repo_data.topics_used)

    def update(self, repo_data):
        # Amount of bytes written in this language in the current repository instance
        byte_size = repo_data.language_dictionary[self.language_name]
        # Dictionary of language combos that include this language in the key with all values set to 1
        lang_combos = [' '.join(combo) for combo in repo_data.language_combinations if self.language_name in combo]
        # self.create_combo_dict(repo_data.language_combinations, self.language_name)
        # List of all the keys from 'language_dict' sorted by their byte sizes (Max Value First)
        lang_byte_order = Process_Data.sort_dictionary_into_list(repo_data.language_dictionary, True)
        # Locates the Index of this language in the  list ands one for actual positioning
        current_ordering = lang_byte_order.index(self.language_name) + 1
        key = Language_Stats.ALP
        self.selective_update(key=key, repo_data=repo_data, byte_size=byte_size,
                              current_ordering=current_ordering, lang_combos=lang_combos)
        key = Language_Stats.MLP if repo_data.uses_multiple_languages else Language_Stats.SLP
        self.selective_update(key=key, repo_data=repo_data, byte_size=byte_size,
                              current_ordering=current_ordering, lang_combos=lang_combos)

    def object_to_list(self, key):

        # "language name"
        values = [self.language_name]

        # "use count"
        data = self.use_count[key]
        values.append(data)

        # "language combinations"
        data = self.language_combinations[key]
        values.append(data)

        # "topics list"
        data = self.topics_list[key]
        values.append(data)

        # "primary language occurrences"
        data = self.tiers[key].count(1)
        values.append(data)

        # "language tier statistics"
        data = Process_Data.calculate_stats(self.tiers[key])
        values.append(data)

        # "bytes written statistics"
        data = Process_Data.calculate_stats(self.bytes_written[key])
        values.append(data)

        # "byte distribution statistics"
        data = Process_Data.calculate_stats(self.byte_distribution[key])
        values.append(data)

        # "languages used statistics"
        data = Process_Data.calculate_stats(self.languages_used[key])
        values.append(data)

        # "topics used statistics"
        data = Process_Data.calculate_stats(self.topics_used[key])
        values.append(data)

        return values

    def object_to_dict(self, key):
        keys = Language_Stats.Header_Names
        values = self.object_to_list(key)
        return {key: value for key, value in zip(keys, values)}
