##### Collect_RQ1_Data.py #####

from Step1.Collect_Research_Data import Collect_Research_Data
from Step2.Language_Stats import Language_Stats
from Step2.Research_Stats import Research_Stats

class Collect_RQ1_Data(Collect_Research_Data):

    def __init__(self, file_name='Language_Stats', file_path='Data/Step2_Data/'):
        super(Collect_RQ1_Data, self).__init__(file_name=file_name, file_path=file_path)

    def update_statistics(self, current_repository):
        for language in current_repository.language_dict:
            if language not in self.research_data:
                self.research_data[language] = Language_Stats(language)
            self.research_data[language].update(current_repository)

    def get_header(self):
        return Language_Stats.Header_Names

    def write_data(self):
        original_file_name = self.file_name
        for projectType in Research_Stats.Project_Types:
            self.file_name = original_file_name + "_" + projectType
            super(Collect_RQ1_Data, self).write_data()
