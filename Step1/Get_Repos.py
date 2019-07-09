import csv  # Used to export the data from Github's API to a CSV file
from datetime import datetime, timedelta
from time import sleep
import requests  # Used to make HTTP request to Github's API

"""
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
"""

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
    current_repo = 1
    repo_count = len(list_of_repos)
    for repo in list_of_repos:
        if 'languages_url' in repo:
            repo['language'] = http_get_call(repo['languages_url'])
            percent_complete = (current_repo / repo_count) * 100
            print("Percentage Complete (Language): %.2f" % percent_complete)
            current_repo += 1


def http_get_call(url):
    global username
    global password
    result = requests.get(url, auth=(username, password), headers={"Accept": "application/vnd.github.mercy-preview+json"})
    if result.status_code != 200:
        print("Invalid API Call:", result.reason)
        exit()
    return result.json()


# Makes an HTTP Get call to Github to retrieve the repos specified by the api string parameters
def get_page_of_repos(page_num, order_by, star_count, date_updated, date_created):
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
    url = 'https://api.github.com/search/repositories?'\
              + 'q=stars:' + star_count + '+is:public+mirror:false+archived:false'\
              + '+pushed:>=' + date_updated + '+created:>=' + date_created\
              + '&sort=stars&per_page=100&order=' + order_by + '&page=' + str(page_num)  # 4250
    if page_num == 1:
        print(url)
    return http_get_call(url)


def get_repos(date_updated, date_created):
    list_of_repos = []
    orders = ["asc", "desc"]
    stars = ["4281..*", "2350..4280"]
    print("Obtaining Repositories from Github...")
    for star_count in stars:
        for order_by in orders:
            for page_num in range(1, 11, 1):
                # Gets repos from github in json format
                json_repos = get_page_of_repos(page_num, order_by, star_count, date_updated, date_created)
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
    for original_repo in list_of_repos:
        if 'url' in original_repo:
            result = http_get_call(original_repo['url'])
            updated_repo = dict(result)
            updated_repo['score'] = original_repo['score']
            updated_repos.append(updated_repo)
            percent_complete = (current_repo / repo_count) * 100
            print("Percentage Complete (Update): %.2f" % percent_complete)
            current_repo += 1
    return updated_repos


def clean_repos(list_of_repos):
    language_dict = {}
    updated_repos = []
    for repo in list_of_repos:
        repo_langs = dict(repo['language'])
        repo_desc = str(repo['description'])
        if len(repo_langs) > 0 and len(repo_desc) > 5:
            language_dict.update(repo_langs)
            updated_repos.append(repo)

    list_of_repos = updated_repos
    updated_repos = []
    languages = [x.lower() for x in language_dict.keys()]
    for repo in list_of_repos:
        repo['topics'] = clean_topics(repo, languages)
        if len(repo['topics']) > 0:
            updated_repos.append(repo)
    return updated_repos


def clean_topics(repo, str_to_remove):
    topics_list = [x.lower() for x in list(repo['topics'])]
    for string in str_to_remove:
        if string in topics_list:
            topics_list.remove(string)
    return topics_list


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
    sleep(3600)  # one hour
    update_repo_languages(list_of_repos)
    list_of_repos = clean_repos(list_of_repos)
    write_to_csv(list_of_repos, 'Original_Repos')
    '''
    repo_fields_wanted = ['id', 'name', 'full_name', 'created_at', 'pushed_at',
                          'updated_at', 'size', 'has_issues', 'forks',
                          'score', 'open_issues', 'subscribers_count',
                          'stargazers_count', 'language', 'topics',
                          'description', 'html_url', 'url', 'owner']
    '''
    repo_fields_wanted = ['size', 'forks', 'score',
                          'open_issues', 'subscribers_count',
                          'stargazers_count', 'language',
                          'topics', 'description', 'owner']
    list_of_repos = update_repo_fields(list_of_repos, repo_fields_wanted)
    final_repo_count = len(list_of_repos)
    # Writes repo data to csv file
    print("Valid Repositories Remaining %d of %d [%.2f%%]" % (final_repo_count, original_repo_count, (final_repo_count / original_repo_count) * 100))
    write_to_csv(list_of_repos, 'Revised_Repos')
