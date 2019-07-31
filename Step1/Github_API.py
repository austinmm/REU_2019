from Process_Data import Process_Data
from datetime import datetime, timedelta
from time import sleep
import requests
from progressbar import ProgressBar
# Reads/Writes in a CSV formatted file
import csv  # reader()
import sys  # sys.maxsize
# Allows code to read in large CSV files
csv.field_size_limit(sys.maxsize)
# Displays a progress bar while looping through an iterable object

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

class Github_API():

    Fields_Wanted = ['id', 'size', 'forks',
                     'open_issues', 'subscribers_count',
                     'stargazers_count', 'language_dictionary',
                     'topics', 'description', 'owner_type']

    def __init__(self, file_name='Github_Repositories', file_path='Data/Step1_Data/'):
        self.list_of_repositories = []
        self.file_name = file_name
        self.file_path = file_path
        self.date_last_updated = ""
        self.date_created = ""
        self.username = ""
        self.password = ""
        self.orders = ["asc", "desc"]
        self.stars = ["4273..*", "2338..4272", "1569..2337", "1172..1568", "915..1171"]

    def execute_repository_query(self):
        # Gets api header and param values
        self.collect_http_info()
        # Obtains initial 'unclean' repositories
        self.get_repos()
        # Initial amount of 'unclean' repositories obtained
        original_repo_count = len(self.list_of_repositories)
        print("%d Repositories have been read in from Github" % original_repo_count)
        # Updates some of the values and adds new ones for each repository
        self.update_repositories()
        # Updates all of the language of each repository to include all languages used and not just the top one
        list_of_languages = self.update_languages()
        # Changes some of the repository values that need to be further cleaned
        self.clean_repositories(list_of_languages)
        # Removes all the repositories that do not meet the minimum requirements to be deemed 'clean'
        self.remove_invalid_repositories()
        # Obtains and displays the final amount of repositories compared to the starting amount
        final_repo_count = len(self.list_of_repositories)
        print("Valid Repositories Remaining %d of %d [%.2f%%]" % (final_repo_count, original_repo_count,
                                                                  (final_repo_count / original_repo_count) * 100))
        Process_Data.store_data(file_path=self.file_path, file_name='Repository_List', data=self.list_of_repositories)
        self.write_data()

    def update_repositories(self):
        print("Updating Repository Data...")
        pbar = ProgressBar()
        index = 0
        for repo in pbar(self.list_of_repositories):
            url = repo['url']
            result = self.http_get_call(url)
            self.list_of_repositories[index] = dict(result)
            index += 1

    def update_languages(self):
        print("Updating Repository Language Data...")
        language_dict = {}
        pbar = ProgressBar()
        for repo in pbar(self.list_of_repositories):
            url = repo['languages_url']
            repo['language'] = self.http_get_call(url)
            language_dict.update(repo['language'])
        return [lang.lower() for lang in language_dict.keys()]

    def collect_http_info(self):
        self.get_basic_auth()
        self.get_date_created()
        self.get_date_last_updated()

    def get_date_last_updated(self):
        print("Date Last Updated Time-Span (months): ", end="")
        months = int(input())
        days = months * 30
        date = datetime.today() - timedelta(days=days)
        self.date_last_updated = date.strftime("%Y-%m-%d")

    def get_date_created(self):
        print("Date Created Time-Span (years): ", end="")
        years = int(input())
        days = years * 365.24
        date = datetime.today() - timedelta(days=days)
        self.date_created = date.strftime("%Y-%m-%d")

    def get_basic_auth(self):
        print("Github Username: ", end="")
        self.username = str(input())
        print("Github Password: ", end="")
        self.password = str(input())

    def remove_invalid_repositories(self):
        updated_repos = []
        for repo in self.list_of_repositories:
            language_count = len(repo['language_dictionary'])
            topics_count = len(repo['topics'])
            character_count = len(str(repo['description']))
            if language_count > 0 and character_count > 5 and topics_count > 0:
                updated_repos.append(repo)
        self.list_of_repositories = updated_repos

    def clean_repositories(self, langs):
        index = 0
        for repo in self.list_of_repositories:
            # Makes all topics lowercase
            topics = [topic.lower() for topic in repo['topics']]
            # Removes all topics that are just programming language names
            repo['topics'] = [topic for topic in topics if topic not in langs]
            # Makes all languages lowercase
            repo['language_dictionary'] = {language.lower(): val for language, val in repo['language'].items()}
            # Makes all descriptions proper strings
            repo['description'] = str(repo['description'])
            # Sets 'owner' field to owner's 'type'
            repo['owner_type'] = repo['owner']['type']
            self.list_of_repositories[index] = {field: repo[field] for field in Github_API.Fields_Wanted}
            index += 1

    def http_get_call(self, url):
        result = requests.get(url,
                              auth=(self.username, self.password),
                              headers={"Accept": "application/vnd.github.mercy-preview+json"})
        if result.status_code != 200:
            print("Status Code %s: %s" % (result.status_code, result.reason))
            # Sleeps program for one hour and then makes call again when api is unrestricted
            sleep(1200)
            return self.http_get_call(url)
        return result.json()

    def get_page_of_repos(self, page_num, order_by, star_count):
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
        url = 'https://api.github.com/search/repositories?' \
              + 'q=stars:' + star_count + '+is:public+mirror:false+archived:false' \
              + '+pushed:>=' + self.date_last_updated + '+created:>=' + self.date_created \
              + '&sort=stars&per_page=100&order=' + order_by + '&page=' + str(page_num)  # 4250
        if page_num == 1:
            print(url)
        return self.http_get_call(url)

    def get_repos(self):
        print("Obtaining Repositories from Github...")
        for star_count in self.stars:
            for order_by in self.orders:
                # Reads in 100 repositories from 10 pages resulting in 1000 repositories
                for page_num in range(1, 11, 1):
                    # Gets repos from github in json format
                    json_repos = self.get_page_of_repos(page_num, order_by, star_count)
                    # json_repos['items'] = list of repo dictionary objects OR is not a valid key
                    if 'items' in json_repos:
                        # Append new repos to the end of 'list_of_repositories'
                        repos = json_repos['items']
                        self.list_of_repositories += repos
                    else:
                        # If 'items' is not a valid key then there are no more repos to read in
                        break

    def write_data(self):
        print("Writing Data to CSV File...")
        file = self.file_path + self.file_name + '.csv'
        with open(file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            # Writes the dictionary keys to the csv file
            writer.writerow(Github_API.Fields_Wanted)
            # Writes all the values of each index of dict_repos as separate rows in the csv file
            for repository in self.list_of_repositories:
                # If the repo is not a multiple-language project then we ignore it
                row = repository.values()
                writer.writerow(row)
        csv_file.close()

