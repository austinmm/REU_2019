from Step3.RQ1_Results import RQ1_Results
from Step3.RQ2_Results import RQ2_Results
from Step3.Display_Data import Display_Data
from Step2.Research_Stats import Research_Stats

def RQ1_1(research_data):
    Size_of_Bins = 1
    Display_Results_By = "Probability"  # "Count", "Probability"
    array = research_data.languages_used_distribution()
    Display_Data.plotly_create_histogram(
        array,
        Size_of_Bins,
        "Languages Used",
        Display_Results_By == "Probability"
    )


if __name__ == '__main__':
    print("Which Research Question Would you like to Display Data for?\n1.) RQ1\n2.) RQ2\nChoice:", end=' ')
    choice = int(input())
    research_data = None
    input_path = '../Data/Step2_Data/'
    output_path = '../Data/Step3_Data/'
    file_name = ""
    if choice == 1:
        print("Display RQ1 Data for...\n1.) All-Languages\n2.) Single-Languages\n3.) Multiple-Languages\nChoice:", end=' ')
        choice = int(input()) - 1
        file_name = Research_Stats.Project_Types[choice]
        research_data = RQ1_Results(input_path, output_path)
    elif choice == 2:
        file_name = "Descriptions"
        research_data = RQ2_Results(input_path, output_path)
    research_data.load_data(file_name)
