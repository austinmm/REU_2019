##### RQ2_Results.py #####

# Static class used to process data
from Process_Data import Process_Data
from Step3.Research_Results import Research_Results

class RQ2_Results(Research_Results):

    def __init__(self, input_path='../Data/Step2_Data/', output_path='../Data/Step3_Data/'):
        super(RQ2_Results, self).__init__(input_path, output_path)
        self.description_stats = []

    def load_data(self, file_name="Descriptions"):
        self.description_stats = Process_Data.read_in_data(self.input_path, file_name, "Description")

    def vectorize_strings(self):
        pass