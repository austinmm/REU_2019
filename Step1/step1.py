from Step1.Collect_Repository_Data import Collect_Repository_Data
from Step1.Github_API import Github_API
from Step1.Repository_Stats import Repository_Stats

if __name__ == '__main__':
    Repository_Stats.Combo_Length_Limit = 5
    # Retrieves repo data from Github by page
    github_info = Github_API()
    github_info.execute_repository_query()
    repository_data = Collect_Repository_Data()
    repository_data.process_data(github_info.list_of_repositories)
