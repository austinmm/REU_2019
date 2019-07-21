##### Collect_Research_Data.py #####

from Process_Data import Process_Data
# Allows for abstract classes
import abc  # abc.ABCMeta, @abc.abstractmethod
from progressbar import ProgressBar  # ProgressBar()
# Reads/Writes in a CSV formatted file
import csv  # reader()
import sys  # sys.maxsize
# Allows code to read in large CSV files
csv.field_size_limit(sys.maxsize)
# Displays a progress bar while looping through an iterable object


class Collect_Research_Data(metaclass=abc.ABCMeta):

    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.research_data = {}

    @abc.abstractmethod
    def write_data(self):
        print("Writing Data to CSV File...")
        file = self.file_path + self.file_name + '.csv'
        with open(file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            # Writes the dictionary keys to the csv file
            writer.writerow(self.get_header())
            # Writes all the values of each index of dict_repos as separate rows in the csv file
            for key, value in self.research_data.items():
                # If the repo is not a multiple-language project then we ignore it
                row = value.create_row(key=self.file_name)
                writer.writerow(row)
        csv_file.close()

    @abc.abstractmethod
    def get_header(self):
        print("Abstract Method that is implemented by inheriting classes")

    def save_objects(self):
        Process_Data.store_data(file_path=self.file_path, file_name=self.file_name, data=self.research_data)

    def process_data(self, list_of_repos):
        pbar = ProgressBar()
        for repo in pbar(list_of_repos):
            self.update_statistics(repo)
        self.write_data()
        self.save_objects()

    @abc.abstractmethod
    def update_statistics(self, current_repository):
        print("Abstract Method that is implemented by inheriting classes")
