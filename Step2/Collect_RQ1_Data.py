##### Collect_RQ1_Data.py #####

from Step1.Collect_Research_Data import Collect_Research_Data
from Step2.Language_Stats import Language_Stats

class Collect_RQ1_Data(Collect_Research_Data):

    def __init__(self, file_name='Language_Stats', file_path='Data/Step2_Data/'):
        super(Collect_RQ1_Data, self).__init__(file_name=file_name, file_path=file_path)
        self.project_type = Language_Stats.ALP

    def _update_statistics(self, current_repository):
        if current_repository.languages_used <= Collect_Research_Data.Language_Combination_Limit:
            for language in current_repository.all_languages:
                if language not in self.research_data:
                    self.research_data[language] = Language_Stats(language)
                self.research_data[language].update(current_repository)

    def _get_header(self):
        return Language_Stats.Header_Names

    def _object_to_list(self, value):
        return value.object_to_list(self.project_type)

    def _object_to_dict(self, value):
        return value.object_to_dict(self.project_type)

    def save_data(self):
        original_file_name = self.file_name
        for p_type in Language_Stats.Project_Types:
            self.project_type = p_type
            self.file_name = original_file_name + "_" + self.project_type
            super(Collect_RQ1_Data, self).save_data()

