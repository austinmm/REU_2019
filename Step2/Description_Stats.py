##### Description_Stats.py #####

from Process_Data import Process_Data
from Step2.Research_Stats import Research_Stats
import Process_Data
import nltk; nltk.download("stopwords")
from nltk.corpus import stopwords
from textblob import TextBlob
from langdetect import detect, detect_langs
from textblob.exceptions import NotTranslated

class Description_Stats(Research_Stats):
    Header_Names = ["Description", "Character Count", "Word Count",
                    "Nouns", "Adjectives", "Verbs", "Propositions",
                    "Stop Words", "Complete Word Counts", "Natural Language"
                    "Natural Language Possibilities", "Uses Multiple Languages",
                    "Languages Used", "Main Language", "All Languages",
                    "Language Combinations", "Topics Used", "Topics"]
    Stop_Words = set(stopwords.words('english'))
    # Stop_Words_Split = Stop_Words.split()

    def __init__(self, repo):
        # String sentence describing what the repository does
        self.description = repo.description
        # Set initial translation to original description
        self.translation = self.description
        # The number of characters in the description
        self.character_count = len(self.description)
        # This object is used to find the parts of speech of each word in the description
        text_blob = TextBlob(self.description)
        # The most likely natural language the description was written in
        self.natural_language = detect(self.description) # text_blob.detect_language()
        # A dictionary containing all the possible natural languages, and their percent possibility, the description was written in
        self.natural_language_possibilities = detect_langs(self.description)
        # An attempted translation of the description from its original language to english
        if self.natural_language != "en":
            try:
                self.translation = str(text_blob.translate(from_lang=self.natural_language, to="en"))
                text_blob = TextBlob(self.translation)
            except NotTranslated:
                self.translation = self.description
        # A dictionary of all the words and their appearance count as their value
        self.complete_word_counts = dict(text_blob.word_counts)
        # The amount of words in the description
        self.word_count = len(text_blob.words)
        # Obtains all words part of speech
        self.nouns = []; self.adjectives = []
        self.verbs = []; self.stop_words = []
        self.part_of_speech_tagging(text_blob)
        # Dictionary of languages as keys with values the amount of bytes written in said language
        self.language_dict = repo.language_dictionary
        # String value of the primary language, in bytes written, of the current repo
        self.main_language = repo.main_language
        # Amount of languages used in current repository instance
        self.languages_used = repo.languages_used
        # Dictionary of language combos that include this language in the key with all values set to 1
        self.language_combinations = repo.language_combinations
        # Boolean that represents if this repository uses multiple languages or not
        self.uses_multiple_languages = repo.uses_multiple_languages
        # List of topics used in current repository instance
        self.topics_list = repo.topics_list
        # Amount of topics used in current repository instance
        self.topics_used = repo.topics_used

    def part_of_speech_tagging(self, text_blob):
        # http://rwet.decontextualize.com/book/textblob/
        self.nouns = list(text_blob.noun_phrases)
        for word, tag in text_blob.tags:
            if ('NN' in tag) and (word not in self.nouns):
                self.nouns.append(word)
            if 'JJ' in tag:
                self.adjectives.append(word)
            elif 'VB' in tag:
                self.verbs.append(word)
        # All the stop phrases within the description
        self.stop_words = list(filter(lambda w: w in Description_Stats.Stop_Words, text_blob.words))

    def create_row(self):
        # "Description"
        values = [self.description]

        # "Translation"
        data = self.translation
        values.append(data)

        # "Character Count"
        data = self.character_count
        values.append(data)

        # "Word Count"
        data = self.word_count
        values.append(data)

        # "Nouns"
        data = self.nouns
        values.append(data)

        # "Adjectives"
        data = self.adjectives
        values.append(data)

        # "Verbs"
        data = self.verbs
        values.append(data)

        # "Stop Words"
        data = self.stop_words
        values.append(data)

        # "Complete Word Counts"
        data = self.complete_word_counts
        values.append(data)

        # "Natural Language"
        data = self.natural_language_possibilities
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

        # "All Languages"
        data = list(self.language_dict.keys())
        values.append(data)

        # "Language Combinations"
        data = self.language_combinations
        values.append(data)

        # "Topics Used"
        data = self.topics_used
        values.append(data)

        # "Topics"
        data = self.topics_list
        values.append(data)

        return values