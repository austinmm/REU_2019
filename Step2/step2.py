from Step2.Collect_RQ1_Data import Collect_RQ1_Data
from Step2.Collect_RQ2_Data import Collect_RQ2_Data
from Process_Data import Process_Data


if __name__ == '__main__':
    print("Which Research Question Would you like to Collect/Prepare Data for?\n1.) RQ1\n2.) RQ2\nChoice:", end=' ')
    choice = int(input())
    research_data = None
    file_path = '../Data/Step2_Data/'
    if choice == 1:
        research_data = Collect_RQ1_Data(file_path=file_path)
    elif choice == 2:
        research_data = Collect_RQ2_Data(file_path=file_path)
    list_of_repos = Process_Data.load_data(file_path='../Data/Step2_Data/', file_name='Repository_Stats')
    research_data.process_data(list_of_repos=list_of_repos)
