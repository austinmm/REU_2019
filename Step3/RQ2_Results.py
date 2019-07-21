##### RQ2_Results.py #####

# Static class used to process data
from Process_Data import Process_Data
from Step3.Research_Results import Research_Results
from sklearn.cluster import MiniBatchKMeans, KMeans, MeanShift, estimate_bandwidth
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score

class RQ2_Results(Research_Results):

    def __init__(self, input_path='../Data/Step2_Data/', output_path='../Data/Step3_Data/'):
        super(RQ2_Results, self).__init__(input_path, output_path)
        self.description_stats = []
        self.processed_descriptions = []
        self.load_data()

    def load_data(self, file_name="Descriptions"):
        self.description_stats = Process_Data.read_in_data(self.input_path, file_name, "Description")
        #Process_Data.store_data(file_path=self.output_path, file_name='description_stats', data=self.description_stats)
        self.processed_descriptions = [row.processed_text for row in self.description_stats]
        Process_Data.store_data(file_path=self.output_path, file_name='processed_descriptions', data=self.processed_descriptions)

    def text_feature_extraction(self):
        '''
        max_df: this is the maximum frequency within the documents a given feature can have to be used in the tfi-idf matrix.
            If the term is in greater than 80% of the documents it probably cares little meanining (in the context of film synopses)
        min_df: Here I pass 0.2; the term must be in at least 20% of the document.
        ngram_range: this just means I'll look at unigrams and bigrams
        '''
        vectorizer = TfidfVectorizer(
            # Ignore all words that appear in more than 60% of all documents
            max_df=0.6,
            # Obtains the top 1000 words/phrases instead of using an min_df
            max_features=1000,
            # Normalizes the word/phrase counts
            use_idf=True,
            # Try to strip accents from characters. Using unicode is slightly slower but more comprehensive than 'ascii'
            strip_accents='unicode',
            # Analyzes words and not characters
            analyzer='word',
            # One and Two worded tokens
            ngram_range=(1, 2),
            # These three parameters are set so they do not alter the already tokenized object to be fill/transform
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
            token_pattern=None
        )
        return vectorizer

    def cluster_text(self, cluster_type="km"):
        vectorizer = self.text_feature_extraction()
        tfidf_model = vectorizer.fit_transform(self.processed_descriptions)
        # reduce the features to 2D
        pca = PCA(n_components=2, random_state=0)
        import numpy
        X = tfidf_model.toarray()
        bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)
        model = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        model.fit(X)

        km_model = KMeans(n_clusters=10)
        km_model.fit(tfidf_model)
        score = silhouette_score(tfidf_model, labels=km_model.predict(tfidf_model))
        print("The Silhouette Coefficient [1,-1]: %.5f" % score)
        '''
        # reduce the cluster centers to 2D
        reduced_cluster_centers = pca.transform(km_model.cluster_centers_)
        plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=km_model.predict(tfidf_model))
        plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:, 1], marker='x', s=150, c='b')

        cls = MiniBatchKMeans(n_clusters=10, random_state=0)
        cls.fit(tfidf_model)
        score = silhouette_score(tfidf_model, labels=cls.predict(tfidf_model))
        print("The Silhouette Coefficient [1,-1]: %.5f" % score)
        # reduce the cluster centers to 2D
        reduced_cluster_centers = pca.transform(cls.cluster_centers_)
        plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=cls.predict(tfidf_model))
        plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:, 1], marker='x', s=150, c='b')
        '''

