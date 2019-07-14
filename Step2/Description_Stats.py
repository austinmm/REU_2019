##### Description_Stats.py #####

from Process_Data import Process_Data
from Step2.Research_Stats import Research_Stats
# Wrapper for the nltk library
from textblob import TextBlob


class Description_Stats(Research_Stats):
    Header_Names = ["Description", "Natural Language", "Subjects",
                    "Processed Text", "Uses Multiple Languages",
                    "Languages Used", "Main Language",
                    "Language Combinations", "Topics Used", "Topics List"]

    def __init__(self, repo):
        text = Process_Data.remove_emojis(repo.description)
        translation = Process_Data.translate_text(text=text)
        # The most likely natural language the description was written in
        self.natural_language = translation.src
        # String sentence describing what the repository does
        self.description = translation.text.lower()
        text_blob = TextBlob(self.description)
        # Obtains all nouns and noun phrases found in the description using TextBlobs nlp tagging
        self.subjects = list(text_blob.noun_phrases)
        # Obtains a prepared TextBlob object to apply nlp algorithms to description
        self.processed_text = Process_Data.clean_text_for_nlp(self.description)
        # Boolean that represents if this repository uses multiple languages or not
        self.uses_multiple_languages = repo.uses_multiple_languages
        # Amount of languages used in current repository instance
        self.languages_used = repo.languages_used
        # String value of the primary language, in bytes written, of the current repo
        self.main_language = repo.main_language
        # Dictionary of language combos that include this language in the key with all values set to 1
        self.language_combinations = repo.language_combinations + [lang for lang in repo.language_dictionary]
        # Amount of topics used in current repository instance
        self.topics_used = repo.topics_used
        # List of topics used in current repository instance
        self.topics_list = repo.topics_list

    def create_row(self, key=''):
        # "Description"
        values = [self.description]

        # "Natural Language"
        data = self.natural_language
        values.append(data)

        # "Subjects"
        data = self.subjects
        values.append(data)

        # "Processed Text"
        data = self.processed_text
        values.append(data)

        # "Uses Multiple-Languages"
        data = self.uses_multiple_languages
        values.append(data)

        # "Languages Used"
        data = self.languages_used
        values.append(data)

        # "Main Language"
        data = self.main_language
        values.append(data)

        # "Language Combinations"
        data = self.language_combinations
        values.append(data)

        # "Topics Used"
        data = self.topics_used
        values.append(data)

        # "Topics List"
        data = self.topics_list
        values.append(data)

        return values