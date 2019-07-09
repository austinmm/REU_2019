##### Collect_RQ1_Data.py #####

from Step2.Collect_Research_Data import Collect_Research_Data
from Step2.Language_Stats import Language_Stats
from Step2.Research_Stats import Research_Stats
# Reads/Writes in a CSV formatted file
import csv  # reader()
import sys  # sys.maxsize
# Allows code to read in large CSV files
csv.field_size_limit(sys.maxsize)

class Collect_RQ1_Data(Collect_Research_Data):

    def __init__(self, input_path='../Data/Step1_Data/', output_path='../Data/Step2_Data/', load_repository_stats=False):
        super(Collect_RQ1_Data, self).__init__(input_path, output_path, load_repository_stats)
        self.languages_stats = {}

    def update_statistics(self, current_repository):
        super(Collect_RQ1_Data, self).update_statistics(current_repository)
        for language in current_repository.language_dict:
            if language not in self.languages_stats:
                self.languages_stats[language] = Language_Stats(language)
            self.languages_stats[language].update(current_repository)

    def write_data(self):
        super(Collect_RQ1_Data, self).write_data()
        # Creates/Overwrites a csv file to write to
        print("Writing Language Data to CSV Files...")
        for projectType in Research_Stats.Project_Types:
            file_name = self.output_path + projectType + '.csv'
            with open(file_name, 'w') as csv_file:
                writer = csv.writer(csv_file)
                # Writes the dictionary keys to the csv file
                writer.writerow(Language_Stats.Header_Names)
                # Writes all the values of each index of dict_repos as separate rows in the csv file
                for language, lang_object in self.languages_stats.items():
                    # If the repo is not a multiple-language project then we ignore it
                    row = lang_object.create_row(projectType)
                    writer.writerow(row)
            csv_file.close()
            print("Finished Writing Language Data to '%s.csv'" % file_name)