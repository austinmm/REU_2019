from Step2.Collect_RQ1_Data import Collect_RQ1_Data
from Step2.Collect_RQ2_Data import Collect_RQ2_Data
from Step1.Repository_Stats import Repository_Stats
from Process_Data import Process_Data



if __name__ == '__main__':
    Repository_Stats.Combo_Length_Limit = 5
    print("Which Research Question Would you like to Collect/Prepare Data for?\n1.) RQ1\n2.) RQ2\nChoice:", end=' ')
    choice = int(input())
    research_data = None
    input_path = '../Data/Step1_Data/'
    output_path = '../Data/Step2_Data/'
    load_repository_stats = True
    if choice == 1:
        research_data = Collect_RQ1_Data(input_path, output_path)
    elif choice == 2:
        research_data = Collect_RQ2_Data(input_path, output_path)
    list_of_repos = Process_Data.load_data('Data/Step1_Data/Repository_Stats')
    research_data.process_data(list_of_repos=list_of_repos)
    valid_combination_percent = research_data.valid_language_combination_percent()
    print("%.2f%% of repositories used %d or less languages"
          % (valid_combination_percent, Repository_Stats.Combo_Length_Limit)
    )