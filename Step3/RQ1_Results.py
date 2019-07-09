##### RQ1_Results.py #####

# Static class used to process data
from Process_Data import Process_Data
from Step3.Research_Results import Research_Results
class RQ1_Results(Research_Results):

    def __init__(self, input_path='../Data/Step2_Data/', output_path='../Data/Step3_Data/'):
        super(RQ1_Results, self).__init__(input_path, output_path)
        self.languages_stats = {}

    def load_data(self, file_name):
        values = Process_Data.read_in_data(self.input_path, file_name, "Language")
        keys = [x.Language_Name for x in values]
        self.languages_stats = Process_Data.create_dictionary(keys, values)

    # Languages Used Distribution
    def languages_used_distribution(self):
        return [x.Languages_Used for x in self.repository_stats]

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