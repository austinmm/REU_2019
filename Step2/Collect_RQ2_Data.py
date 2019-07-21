##### Collect_RQ2_Data.py #####

from Step1.Collect_Research_Data import Collect_Research_Data
from Step2.Description_Stats import Description_Stats

class Collect_RQ2_Data(Collect_Research_Data):

    def __init__(self, file_name="Description_Stats", file_path='../Data/Step2_Data/'):
        super(Collect_RQ2_Data, self).__init__(file_name=file_name, file_path=file_path)

    def update_statistics(self, current_repository):
        repo_id = current_repository.id
        self.research_data[repo_id] = Description_Stats(current_repository)

    def get_header(self):
        return Description_Stats.Header_Names

    def write_data(self):
        super(Collect_RQ2_Data, self).write_data()
