from Step1.Collect_Research_Data import Collect_Research_Data
from Step1.Repository_Stats import Repository_Stats
from Process_Data import Process_Data

class Collect_Repository_Data(Collect_Research_Data):

    def __init__(self, file_name='Repository_Stats', file_path='Data/Step2_Data/'):
        super(Collect_Repository_Data, self).__init__(file_name=file_name, file_path=file_path)
        self.all_language_combinations = {}

    def _update_statistics(self, current_repository):
        current_repository = Repository_Stats(current_repository)
        repo_id = current_repository.id
        self.research_data[repo_id] = current_repository
        for combo in current_repository.language_combinations:
            combo = ' '.join(combo)
            self.all_language_combinations[combo] = self.all_language_combinations.get(combo, 0) + 1

    def save_data(self):
        super(Collect_Repository_Data, self).save_data()
        Process_Data.store_data(file_path=self.file_path,
                                file_name='Programming_Language_Combination_List',
                                data=self.all_language_combinations)

    def _object_to_list(self, value):
        return super(Collect_Repository_Data, self)._object_to_list(value)

    def _object_to_dict(self, value):
        return super(Collect_Repository_Data, self)._object_to_dict(value)

    def _get_header(self):
        return super(Collect_Repository_Data, self)._get_header()


