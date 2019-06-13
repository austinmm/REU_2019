import csv  # Used to export the data from Github's API to a CSV file
from datetime import datetime, timedelta
'''
* To use the 'import requests' you must install the library first
* Ensure that you have pip installed, if not then... "pip install --user pipenv"
* Now install the 'requests' Library... "pipenv install requests"
'''
import requests  # Used to make HTTP request to Github's API

'''
       * Overall Github API V3 Guide: https://developer.github.com/v3/
       
       * Repository Search Query Parameters: https://help.github.com/en/articles/searching-for-repositories

           stars: >= n           -> matches repositories with the at least n stars
           pushed: >= n          -> matched repositories that have last pushed on or after yyyy-mm-dd
           created: >= n         -> matched repositories that were created on or after yyyy-mm-dd
           is: public/private    -> matches repositories that obey this condition
           mirror: false/true    -> matches repositories that obey this boolean
           archived: false/true  -> matches repositories that obey this boolean

       * API Parameters:

           https://developer.github.com/v3/search/#constructing-a-search-query
           sort = stars, forks, help-wanted-issues, or updated
           order = desc, asc

           https://developer.github.com/v3/#pagination
           page: n
           per_page: 1-100
'''

# ***** Global Variables *****
username = ""
password = ""

def write_to_csv(list_of_repos, file_name):
    # Creates/Overwrites a csv file to write to
    print("Writing Repositories to CSV File...")
    with open(file_name + '.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        # Writes the dictionary keys to the csv file
        csv_header = list_of_repos[0].keys()
        writer.writerow(csv_header)
        # Writes all the values of each index of dict_repos as separate rows in the csv file
        for repo in list_of_repos:
            # If the repo is not a multi-language project then we ignore it
            writer.writerow(repo.values())
    print("Finished Writing Repositories to '%s.csv'" % file_name)


def update_repo_languages(list_of_repos):
    print("Updating Repository Language Data...")
    updated_repos = []
    current_repo = 1
    repo_count = len(list_of_repos)
    for repo in list_of_repos:
        if 'languages_url' in repo:
            api_string = repo['languages_url']
            global username; global password
            result = requests.get(api_string, auth=(username, password))
            repo['language'] = result.json()
            # If the repo is not a multi-language project then we return false
            if len(repo['language']) > 1:
                updated_repos.append(repo)
            percent_complete = (current_repo / repo_count) * 100
            print("Percentage Complete: %.2f" % percent_complete)
            current_repo += 1
    return updated_repos


# Makes an HTTP Get call to Github to retrieve the repos specified by the api string parameters
def get_page_of_repos(page_num, order_by, date_updated, date_created):
    '''
        This call will get all <public> repositories on github that...
        * Have <4250> or more stars
        * Were pushed/updated on or after <date_updated>
        * Were created no later than <date_created>
        * Are <not> mirrored repos
        * Are <not> archived repos
        The resulting <100> repos will be on page <n> ordered by...
        * Their <star> count
        * In <desc, asc> order
    '''
    api_str = 'https://api.github.com/search/repositories?'\
              + 'q=stars:>=4250+is:public+mirror:false+archived:false'\
              + '+pushed:>=' + date_updated + '+created:>=' + date_created\
              + '&sort=stars&per_page=100&order=' + order_by + '&page=' + str(page_num)
    if page_num == 1:
        print(api_str)
    global username; global password
    result = requests.get(api_str, auth=(username, password), headers={"Accept": "application/vnd.github.mercy-preview+json"})#topics
    return result.json()


def get_repos(date_updated, date_created):
    list_of_repos = []
    orders = ["asc", "desc"]
    print("Obtaining Repositories from Github...")
    for order_by in orders:
        for page_num in range(1, 11, 1):
            # Gets repos from github in json format
            json_repos = get_page_of_repos(page_num, order_by, date_updated, date_created)
            # json_repos['items'] = list of repo dictionary objects OR is not a valid key
            if 'items' in json_repos:
                # If 'items' is a key in the 'json_repos' dictionary then add new repos to the end of 'list_of_repos'
                list_of_repos += json_repos['items']
            else:
                # If 'items' is not a valid key in the 'json_repos' dictionary then there are no more repos to read in
                break
    print("%d Repositories have been read in from Github" % len(list_of_repos))
    return list_of_repos


def update_repo_data(list_of_repos):
    print("Updating Repository Data...")
    updated_repos = []
    current_repo = 1
    repo_count = len(list_of_repos)
    for repo in list_of_repos:
        if 'url' in repo:
            api_string = repo['url']
            global username; global password
            result = requests.get(api_string, auth=(username, password), headers={"Accept": "application/vnd.github.mercy-preview+json"})
            updated_repo = dict(result.json())
            updated_repo['score'] = repo['score']
            # If the repo is not a multi-language project then we return false
            if len(repo['topics']) > 0:
                updated_repos.append(repo)
            percent_complete = (current_repo / repo_count) * 100
            print("Percentage Complete: %.2f" % percent_complete)
            current_repo += 1
    return updated_repos


def update_repo_fields(list_of_repos, repo_fields_wanted):
    updated_repos = []
    for repo in list_of_repos:
        updated_repo = {}
        for field in repo_fields_wanted:
            if field in repo:
                updated_repo[field] = repo[field]
            else:
                print("Invalid Field: '%s'" % field)
        updated_repos.append(updated_repo)
    return updated_repos


def repo_updated_date():
    print("Date Last Updated Time-Span (months): ", end="")
    months = int(input())
    days = months * 30
    date = datetime.today() - timedelta(days=days)
    return date.strftime("%Y-%m-%d")


def repo_created_date():
    print("Date Created Time-Span (years): ", end="")
    years = int(input())
    days = years * 365.24
    date = datetime.today() - timedelta(days=days)
    return date.strftime("%Y-%m-%d")

def basic_auth():
    print("Github Username: ", end="")
    global username
    username = str(input())
    print("Github Password: ", end="")
    global password
    password = str(input())


if __name__ == '__main__':
    # Retrieves repo data from Github by page
    basic_auth()
    date_updated = repo_updated_date()
    date_created = repo_created_date()
    list_of_repos = get_repos(date_updated, date_created)
    original_repo_count = len(list_of_repos)
    list_of_repos = update_repo_data(list_of_repos)
    list_of_repos = update_repo_languages(list_of_repos)
    write_to_csv(list_of_repos, 'Github_Repos')
    repo_fields_wanted = ['id', 'name', 'full_name', 'created_at', 'pushed_at',
                          'updated_at', 'size', 'has_issues', 'forks',
                          'score', 'open_issues', 'subscribers_count',
                          'stargazers_count', 'language', 'topics',
                          'description', 'html_url', 'url', 'owner']
    list_of_repos = update_repo_fields(list_of_repos, repo_fields_wanted)
    final_repo_count = len(list_of_repos)
    # Writes repo data to csv file
    print("Valid Repositories Remaining %d of %d [%.2f%%]" % (final_repo_count, original_repo_count, (final_repo_count / original_repo_count) * 100))
    write_to_csv(list_of_repos, 'Revised_Repos')
