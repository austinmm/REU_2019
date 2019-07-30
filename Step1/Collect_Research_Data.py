##### Collect_Research_Data.py #####

from Process_Data import Process_Data
# Allows for abstract classes
import abc  # abc.ABCMeta, @abc.abstractmethod
from progressbar import ProgressBar  # ProgressBar()
from types import SimpleNamespace
# Reads/Writes in a CSV formatted file
import csv  # reader()
import sys  # sys.maxsize
# Allows code to read in large CSV files
csv.field_size_limit(sys.maxsize)
# Displays a progress bar while looping through an iterable object

class Collect_Research_Data(metaclass=abc.ABCMeta):

    Language_Combination_Limit = 20

    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.research_data = {}

    @abc.abstractmethod
    def save_data(self):
        self.__write_data_to_csv()
        self.__serialize_objects()

    def __write_data_to_csv(self):
        print("Writing Data to CSV File...")
        file = self.file_path + self.file_name + '.csv'
        with open(file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            # Writes the dictionary keys to the csv file
            writer.writerow(self._get_header())
            # Writes all the values of each index of dict_repos as separate rows in the csv file
            for key, value in self.research_data.items():
                row = self._object_to_list(value)
                writer.writerow(row)
        csv_file.close()

    @abc.abstractmethod
    def _object_to_list(self, value):
        return list(value.__dict__.values())

    @abc.abstractmethod
    def _object_to_dict(self, value):
        return value.__dict__

    @abc.abstractmethod
    def _get_header(self):
        return list(list(self.research_data.values())[0].__dict__.keys())

    def __serialize_objects(self):
        print("Storing Serialized Object in File...")
        # Converts all class objects to list of values
        serialized_objects = {key: self._object_to_dict(value) for key, value in self.research_data.items()}
        # Pickles data
        Process_Data.store_data(file_path=self.file_path, file_name=self.file_name, data=serialized_objects)

    def process_data(self, list_of_repos):
        pbar = ProgressBar()
        for current_repository in pbar(list_of_repos):
            current_repository = SimpleNamespace(**current_repository)
            self._update_statistics(current_repository)

    @abc.abstractmethod
    def _update_statistics(self, current_repository):
        print("Abstract Method that is implemented by inheriting classes")
