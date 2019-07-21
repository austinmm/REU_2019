##### Repository_Stats.py #####
from Step2.Research_Stats import Research_Stats
from Process_Data import Process_Data


class Repository_Stats(Research_Stats):

    Header_Names = ["id", "uses multiple languages", "languages used", "main language",
                    "language dictionary", "valid language combinations",
                    "language combinations", "topics used",
                    "topics list", "description", "owner type", "open issues",
                    "stars", "watchers", "forks"]

    # Max amount of languages any one repository can have to be used to compute the language combinations
    Combo_Length_Limit = 18

    def __init__(self, repo):
        # This is a key that is unique to this repository only
        self.id = repo.id
        # Dictionary of languages as keys with values the amount of bytes written in said language
        self.language_dictionary = repo.language_dictionary
        # Amount of bytes written in this language in the current repository instance
        self.byte_size = sum(list(self.language_dictionary.values()))
        # String value of the primary language, in bytes written, of the current repo
        self.main_language = Process_Data.calculate_top_dict_key(self.language_dictionary, None)
        # Amount of languages used in current repository instance
        self.languages_used = len(self.language_dictionary)
        # Boolean that represents if this repository uses multiple languages or not
        self.uses_multiple_languages = True if self.languages_used > 1 else False
        # Dictionary of language combos that include this language in the key with all values set to 1
        self.language_combinations = Process_Data.create_unique_combo_list(
            self.language_dictionary, self.languages_used,
            max_combo_count=Repository_Stats.Combo_Length_Limit, min_combo_count=2
        )
        # List of topics used in current repository instance
        self.topics_list = repo.topics
        # Amount of topics used in current repository instance
        self.topics_used = len(self.topics_list)
        # The description of the repository
        self.description = str(repo.description)
        # The type of owner of the repository
        self.owner_type = repo.owner_type
        # The amount of open issues the repository has
        self.open_issues = repo.open_issues
        # The amount of stars the repository has
        self.stars = repo.stargazers_count
        # The amount of people who are watching the repository
        self.watchers = repo.subscribers_count
        # The amount of times the repository was forked
        self.forks = repo.forks
        # This boolean indicates if the repository language use count was valid to compute language_combinations
        self.valid_language_combinations = True if self.languages_used <= Repository_Stats.Combo_Length_Limit else False

    def create_row(self, key=''):
        # "id"
        values = [self.id]

        # "uses multiple languages"
        data = self.uses_multiple_languages
        values.append(data)

        # "languages used"
        data = self.languages_used
        values.append(data)

        # "main language"
        data = self.main_language
        values.append(data)

        # "language dictionary"
        data = self.language_dictionary
        values.append(data)

        # "valid language combinations"
        data = self.valid_language_combinations
        values.append(data)

        # "language combinations"
        data = self.language_combinations
        values.append(data)

        # "topics used"
        data = self.topics_used
        values.append(data)

        # "topics list"
        data = self.topics_list
        values.append(data)

        # "description"
        data = self.description
        values.append(data)

        # "owner type"
        data = self.owner_type
        values.append(data)

        # "open issues"
        data = self.open_issues
        values.append(data)

        # "stars"
        data = self.stars
        values.append(data)

        # "watchers"
        data = self.watchers
        values.append(data)

        # "forks"
        data = self.forks
        values.append(data)

        return values