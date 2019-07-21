from Step1.Collect_Research_Data import Collect_Research_Data
from Step1.Repository_Stats import Repository_Stats
from Step1.Github_API import Github_API
from Process_Data import Process_Data


class Collect_Repository_Data(Collect_Research_Data):

    def __init__(self, file_name='Repository_Stats', file_path='Data/Step2_Data/'):
        super(Collect_Repository_Data, self).__init__(file_name=file_name, file_path=file_path)
        keys = [Github_API.Fields_Wanted.index(field) for field in Github_API.Fields_Wanted]
        self.tuple_keys = Process_Data.create_dictionary(keys=keys,
                                                         values=Github_API.Fields_Wanted)

    def update_statistics(self, current_repository):
        current_repository = Process_Data.convert_to_named_tuple(
            class_name="Repository",
            dictionary=self.tuple_keys,
            values=list(current_repository.values())
        )
        current_repository = Repository_Stats(current_repository)
        repo_id = current_repository.id
        self.research_data[repo_id] = current_repository

    def get_header(self):
        return Repository_Stats.Header_Names

    def write_data(self):
        super(Collect_Repository_Data, self).write_data()

