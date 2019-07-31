##### Description_Stats.py #####

from Process_Data import Process_Data
# Wrapper for the nltk library
from textblob import TextBlob


class Description_Stats():
    '''
    Header_Names = ["repository id", "description", "natural language",
                    "subjects", "processed text", "uses multiple languages",
                    "languages used", "main language",
                    "language combinations", "topics used", "topics list"]
    '''
    def __init__(self, repo):
        self.repository_id = repo.id
        translation = Process_Data.translate_text(text=repo.description)
        # The most likely natural language the description was written in
        self.natural_language = translation.src
        # String sentence describing what the repository does
        self.description = Process_Data.clean_text(translation.text)
        text_blob = TextBlob(self.description)
        # Obtains all nouns and noun phrases found in the description using TextBlobs nlp tagging
        self.subjects = list(text_blob.noun_phrases)
        # Obtains a prepared TextBlob object to apply nlp algorithms to description
        self.processed_text = Process_Data.process_text_for_nlp(self.description)
        # Boolean that represents if this repository uses multiple languages or not
        self.uses_multiple_languages = repo.uses_multiple_languages
        # Amount of languages used in current repository instance
        self.languages_used = repo.languages_used
        # String value of the primary language, in bytes written, of the current repo
        self.main_language = repo.main_language
        # List of language combos
        self.language_combinations = [' '.join(combo) for combo in repo.language_combinations]
        # Amount of topics used in current repository instance
        self.topics_used = repo.topics_used
        # List of topics used in current repository instance
        self.topics_list = repo.topics_list

    '''
    def create_row(self, key=''):
        # "Repository Id"
        values = [self.repository_id]

        # "Description"
        data = self.description
        values.append(data)

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
    '''