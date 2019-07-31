from Step1.Collect_Repository_Data import Collect_Repository_Data
from Step1.Github_API import Github_API
from Step2.Research_Stats import Research_Stats

if __name__ == '__main__':
    Research_Stats.Combo_Length_Limit = 20
    # Retrieves repo data from Github by page
    github_info = Github_API()
    github_info.execute_repository_query()
    repository_data = Collect_Repository_Data()
    repository_data.process_data(github_info.list_of_repositories)
