##### Collect_RQ2_Data.py #####

from Step2.Collect_Research_Data import Collect_Research_Data
from Step2.Description_Stats import Description_Stats
# Reads/Writes in a CSV formatted file
import csv  # reader()
import sys  # sys.maxsize
# Allows code to read in large CSV files
csv.field_size_limit(sys.maxsize)


class Collect_RQ2_Data(Collect_Research_Data):

    def __init__(self, input_path='../Data/Step1_Data/', output_path='../Data/Step2_Data/', load_repository_stats=False):
        super(Collect_RQ2_Data, self).__init__(input_path, output_path, load_repository_stats)
        self.description_stats = {}

    def update_statistics(self, current_repository):
        super(Collect_RQ2_Data, self).update_statistics(current_repository)
        description = current_repository.description
        self.description_stats[description] = Description_Stats(current_repository)

    def write_data(self):
        super(Collect_RQ2_Data, self).write_data()
        # Creates/Overwrites a csv file to write to
        print("Writing Description Data to CSV Files...")
        file_name = self.output_path + 'Descriptions.csv'
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            # Writes the dictionary keys to the csv file
            writer.writerow(Description_Stats.Header_Names)
            # Writes all the values of each index of dict_repos as separate rows in the csv file
            for description, desc_object in self.description_stats.items():
                row = desc_object.create_row()
                writer.writerow(row)
        csv_file.close()
        print("Finished Writing Description Data to '%s.csv'" % file_name)