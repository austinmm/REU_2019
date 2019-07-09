##### Collect_Research_Data.py #####

# Allows for abstract classes
import abc  # abc.ABCMeta, @abc.abstractmethod
# Static class used to process data
from Process_Data import Process_Data
from Step2.Repository_Stats import Repository_Stats
# Reads/Writes in a CSV formatted file
import csv  # reader()
import sys  # sys.maxsize
# Allows code to read in large CSV files
csv.field_size_limit(sys.maxsize)
# Displays a progress bar while looping through an iterable object
from progressbar import ProgressBar  # ProgressBar()


class Collect_Research_Data(metaclass=abc.ABCMeta):

    def __init__(self, input_path, output_path, load_repository_stats):
        self.output_path = output_path
        self.input_path = input_path
        self.repositories_stats = []
        self.file_name = "Revised_Repos"
        if load_repository_stats:
            self.file_name = "Repositories"

    def valid_language_combination_percent(self):
        valid_language_combinations = list(filter(
            lambda repo: repo.valid_language_combinations == True, self.repositories_stats)
        )
        percent_valid = (len(valid_language_combinations) / len(self.repositories_stats)) * 100
        return percent_valid

    @abc.abstractmethod
    def write_data(self):
        print("Writing Repository Data to CSV File...")
        file_name = self.output_path + 'Repositories.csv'
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file)
            # Writes the dictionary keys to the csv file
            writer.writerow(Repository_Stats.Header_Names)
            # Writes all the values of each index of dict_repos as separate rows in the csv file
            for repo in self.repositories_stats:
                # If the repo is not a multiple-language project then we ignore it
                row = repo.create_row()
                writer.writerow(row)
        csv_file.close()
        print("Finished Writing Repository Data to '%s.csv'" % file_name)

    def get_list_of_repos(self):
        # Raw Repository Data
        if self.file_name == "Revised_Repos":
            print("Reading in Raw Github Repositories")
            list_of_repos = Process_Data.read_in_data(self.input_path, self.file_name, "Repository")
            pbar = ProgressBar()
            print("Converting Raw Github Repositories to Repository_Stats Objects")
            list_of_repos = [Repository_Stats(repo) for repo in pbar(list_of_repos)]
        # Repository_Stats Objects
        else:
            print("Reading in Repository_Stats Objects")
            list_of_repos = Process_Data.read_in_data(self.output_path, self.file_name, "Repository")
        return list_of_repos

    def process_data(self):
        list_of_repos = self.get_list_of_repos()
        pbar = ProgressBar()
        for repo in pbar(list_of_repos):
            self.update_statistics(repo)
        self.write_data()

    @abc.abstractmethod
    def update_statistics(self, current_repository):
        self.repositories_stats.append(current_repository)