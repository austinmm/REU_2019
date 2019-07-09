##### Research_Results.py #####

# Static class used to process data
from Process_Data import Process_Data
# Allows for abstract classes
import abc  # abc.ABCMeta, @abc.abstractmethod

class Research_Results(metaclass=abc.ABCMeta):

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.repository_stats = Process_Data.read_in_data(self.input_path,
                                                          "Repositories", "Repository")
    @abc.abstractmethod
    def load_data(self, file_name):
        print("Abstract Method that is implemented by inheriting classes")
