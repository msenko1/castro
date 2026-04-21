import os
import pandas as pd

import seaborn as sn
import matplotlib.pyplot as plt
import re
import math
import numpy as np
from collections import defaultdict

from porter_stemmer import PorterStemmer

def prep_castro_docs(csv_path, response_variable, use_order=True):
    print(f"Reading data from {csv_path}...")
    df = pd.read_csv(csv_path)

    document_criteria = [
        ('castro_res', 'mission', 2),
        ('castro_res', 'castro', 1),
        ('castro_res', 'marina', 2),
        ('castro_vis', 'mission', 2),
        ('castro_vis', 'castro', 1),
        ('castro_vis', 'marina', 2),
        ('mission_res', 'mission', 1),
        ('mission_res', 'mission', 2),
        ('mission_res', 'castro', 1),
        ('mission_res', 'castro', 2),
        ('marina_res', 'castro', 1),
        ('marina_res', 'castro', 2),
        ('marina_res', 'marina', 1),
        ('marina_res', 'marina', 2)
    ]

    documents = []
    document_titles = []

    # remove order dimension if not using it
    if not use_order:
        document_criteria = list(set((a, b) for a, b, _ in document_criteria))

    for crit in document_criteria:

        if use_order:
            fieldsite, response_site, order = crit
            subset = df.loc[
                (df.fieldsite == fieldsite) &
                (df.response_site == response_site) &
                (df.order == order)
            ]
            title = f"{fieldsite}_{response_site}_{order}"

        else:
            fieldsite, response_site = crit
            subset = df.loc[
                (df.fieldsite == fieldsite) &
                (df.response_site == response_site)
            ]
            title = f"{fieldsite}_{response_site}"

        responses = subset[response_variable].tolist()
        document = " ".join(responses)

        documents.append(document)
        document_titles.append(title)

        print(f"Prepared document for {title} with {len(responses)} responses.")

    return documents, document_titles

def save_docs_to_txt(documents, document_titles, output_dir):
    raw_dir = os.path.join(output_dir, "raw")

    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir)

    for title, doc in zip(document_titles, documents):
        with open(os.path.join(raw_dir, f"{title}.txt"), 'w', encoding='utf-8') as f:
            f.write(doc)


class IRSystem:
    def __init__(self):
        # For holding the data - initialized in read_data()
        self.titles = []
        self.docs = []
        self.vocab = []
        # For the text pre-processing.
        self.alphanum = re.compile('[^a-zA-Z0-9]')
        self.p = PorterStemmer()

    def get_uniq_words(self):
        uniq = set()
        for doc in self.docs:
            for word in doc:
                uniq.add(word)
        return uniq

    def __read_raw_data(self, dirname):
        print("Stemming Documents...")

        titles = []
        docs = []
        os.mkdir('%s/stemmed' % dirname)

        # make sure we're only getting the files we actually want
        filenames = []
        for filename in os.listdir('%s/raw' % dirname):
            if filename.endswith(".txt") and not filename.startswith("."):
                filenames.append(filename)

        for i, filename in enumerate(filenames):
            title = filename.split('.')[0]
            print("    Doc %d of %d: %s" % (i + 1, len(filenames), title))
            titles.append(title)
            contents = []
            f = open('%s/raw/%s' % (dirname, filename), 'r', encoding="utf-8")
            of = open('%s/stemmed/%s.txt' % (dirname, title), 'w',
                      encoding="utf-8")
            for line in f:
                # make sure everything is lower case
                line = line.lower()
                # split on whitespace
                line = [xx.strip() for xx in line.split()]
                # remove non alphanumeric characters
                line = [self.alphanum.sub('', xx) for xx in line]
                # remove any words that are now empty
                line = [xx for xx in line if xx != '']
                # stem words
                line = [self.p.stem(xx) for xx in line]
                # add to the document's conents
                contents.extend(line)
                if len(line) > 0:
                    of.write(" ".join(line))
                    of.write('\n')
            f.close()
            of.close()
            docs.append(contents)
        return titles, docs

    def __read_stemmed_data(self, dirname):
        print("Already stemmed!")
        titles = []
        docs = []

        # make sure we're only getting the files we actually want
        filenames = []
        for filename in os.listdir('%s/stemmed' % dirname):
            if filename.endswith(".txt") and not filename.startswith("."):
                filenames.append(filename)

        for i, filename in enumerate(filenames):
            title = filename.split('.')[0]
            titles.append(title)
            contents = []
            f = open('%s/stemmed/%s' % (dirname, filename), 'r',
                     encoding="utf-8")
            for line in f:
                # split on whitespace
                line = [xx.strip() for xx in line.split()]
                # add to the document's conents
                contents.extend(line)
            f.close()
            docs.append(contents)

        return titles, docs

    def read_data(self, dirname):
        """
        Given the location of the 'data' directory, reads in the documents to
        be indexed.
        """
        # NOTE: We cache stemmed documents for speed
        #       (i.e. write to files in new 'stemmed/' dir).

        print("Reading in documents...")
        # dict mapping file names to list of "words" (tokens)
        filenames = os.listdir(dirname)
        subdirs = os.listdir(dirname)
        if 'stemmed' in subdirs:
            titles, docs = self.__read_stemmed_data(dirname)
        else:
            titles, docs = self.__read_raw_data(dirname)

        # Sort document alphabetically by title to ensure we have the proper
        # document indices when referring to them.
        ordering = [idx for idx, title in sorted(enumerate(titles),
                                                 key=lambda xx: xx[1])]

        self.titles = []
        self.docs = []
        numdocs = len(docs)
        for d in range(numdocs):
            self.titles.append(titles[ordering[d]])
            self.docs.append(docs[ordering[d]])

        # Get the vocabulary.
        self.vocab = [xx for xx in self.get_uniq_words()]

    def index(self):
        """
        Build an index of the documents.
        """
        print("Indexing...")
        # ------------------------------------------------------------------
        # TODO: Create an inverted index.
        #       This index should map words to documents and store the count
        #       of how many times each word appears in each document.
        #       Some helpful instance variables:
        #         * self.docs = List of documents
        #         * self.titles = List of titles

        # Note: To avoid having to initialize inv_index manually, we import
        # defaultdict from collections.
        
        # Structure: inv_index[word][doc_id] = term_count
        # Example: inv_index["drawer"] = {24: 8, 33: 2, 7: 1, ...}
        inv_index = defaultdict(lambda: defaultdict(int))
        
        # TODO: Generate inverted index here
        for i in range(len(self.docs)):
            wordlist = self.docs[i]
            for word in wordlist:
                inv_index[word][i] +=1

        self.inv_index = inv_index

        # ------------------------------------------------------------------

        # turn self.docs into a map from ID to bag of words
        id_to_bag_of_words = {}
        for d, doc in enumerate(self.docs):
            bag_of_words = set(doc)
            id_to_bag_of_words[d] = bag_of_words

            print(f"Document {d}: {self.titles[d]} with {len(bag_of_words)} unique words.")
            print(bag_of_words)
        self.docs = id_to_bag_of_words
    
    def get_posting(self, word):
        """
        Given a word, this returns the list of document indices (sorted) in
        which the word occurs.
        """
        # ------------------------------------------------------------------
        # TODO: return the list of postings for a word.
        posting = []
        posting = list(self.inv_index[word].keys())
        
        posting.sort()

        return posting
        # ------------------------------------------------------------------
    
    def get_posting_unstemmed(self, word):
        """
        Given a word, this *stems* the word and then calls get_posting on the
        stemmed word to get its postings list. You should *not* need to change
        this function. It is needed for submission.
        """
        word = self.p.stem(word)
        return self.get_posting(word)
    
    def compute_tfidf(self, use_idf=False):
        """
        Compute and store TF-IDF values for words and documents.
        Recall: TF-IDF = (1 + log10(tf)) * log10(N/df)
        where tf = term frequency, N = number of documents, df = document frequency
        """
        print("Calculating tf-idf...")
        self.tfidf = {}
        
        # ------------------------------------------------------------------
        # TODO: Compute TF-IDF values for all word-document pairs.
        #       Store the results in self.tfidf as a nested dictionary:
        #       self.tfidf[word][doc_id] = tfidf_value
        #       
        #       Useful values:
        #         * self.vocab = list of all unique words
        #         * self.inv_index = inverted index (word -> doc -> count)
        #         * len(self.docs) = number of documents (N)

        # YOUR CODE HERE
        self.tfidf = defaultdict(lambda: defaultdict(float))

        for word in self.vocab:
            postings = self.get_posting(word)
            
            df = len(postings)
            idf = df #NOT ACTUAL IDF!

            if use_idf:
                idf = math.log10(len(self.docs)/df)

            tf = float
            
            for doc_id in postings:
                tf = 1+math.log10(self.inv_index[word][doc_id])

                tfidf = tf * idf

                self.tfidf[word][doc_id] = tfidf

        # ------------------------------------------------------------------

    def get_tfidf(self, word, document):
        """
        Return the TF-IDF weight for a word in a specific document.
        """
        # ------------------------------------------------------------------
        # TODO: Return the TF-IDF value for the given word and document index.
        #       Return 0 if the word is not in the vocabulary or not in
        #       the specified document.
        tfidf = 0.0
        if word in self.vocab and document in self.get_posting(word):
            tfidf = self.tfidf[word][document]
        # ------------------------------------------------------------------
        return tfidf

    def get_tfidf_unstemmed(self, word, document):
        """
        Given a word, this *stems* the word and then calls get_tfidf on the
        stemmed word to get its TF-IDF value. You should *not* need to change
        this function. It is needed for submission.
        """
        word = self.p.stem(word)
        return self.get_tfidf(word, document)
    
    def compute_l2_norms(self):
        # Compute and store the L2 norms of each document vector.

        self.doc_norms = defaultdict(float)
        for doc in self.docs:
            l2_norm = 0.0
            for word in self.tfidf:
                if doc in self.tfidf[word]:
                    l2_norm += self.tfidf[word][doc] ** 2
            self.doc_norms[doc] = math.sqrt(l2_norm)

    def compute_dot_product(self, doc1, doc2):
        #Get bag of words for both documents
        bow1 = self.docs[doc1]
        bow2 = self.docs[doc2]
        shared_words = bow1.intersection(bow2)
        if not shared_words:
            return 0.0
        doc1_values = [self.tfidf[word][doc1] for word in shared_words]
        doc2_values = [self.tfidf[word][doc2] for word in shared_words]

        doc1_vector = np.array(doc1_values)
        doc2_vector = np.array(doc2_values)

        doc1_l2_norm = self.doc_norms[doc1]
        doc2_l2_norm = self.doc_norms[doc2]

        if doc1_l2_norm == 0 or doc2_l2_norm == 0:
            return 0.0

        dot_product = np.dot(doc1_vector, doc2_vector)
        cosine_similarity = dot_product / (doc1_l2_norm * doc2_l2_norm)
        return cosine_similarity
    
    def compute_all_dot_products(self):
        self.dot_products = defaultdict(lambda: defaultdict(float))
        num_docs = len(self.docs)
        for i in range(num_docs):
            for j in range(i + 1, num_docs):
                sim = self.compute_dot_product(i, j)
                self.dot_products[i][j] = sim
                self.dot_products[j][i] = sim
    
    def save_similarity_matrix_to_csv(self, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        num_docs = len(self.docs)
        sim_matrix = np.zeros((num_docs, num_docs))
        for i in range(num_docs):
            for j in range(num_docs):
                if i == j:
                    sim_matrix[i][j] = 1.0
                elif j in self.dot_products[i]:
                    sim_matrix[i][j] = self.dot_products[i][j]
                else:
                    sim_matrix[i][j] = 0.0
        df = pd.DataFrame(sim_matrix, index=self.titles, columns=self.titles)

        fig, ax = plt.subplots(figsize=(10, 8))  # make it bigger too
        title_order = [

        # responses about Castro
        "mission_res_castro",
        "marina_res_castro",
        "castro_res_castro",
        "castro_vis_castro",

        # responses about Mission
        "mission_res_mission",
        "castro_res_mission",
        "castro_vis_mission",

        # responses about Marina
        "marina_res_marina",
        "castro_res_marina",
        "castro_vis_marina",
        
    ]
        df_ordered = df.loc[title_order, title_order]
        sn.heatmap(df_ordered, ax=ax).set_title("Micro-category Similarity Heatmap (Term Frequency-Inverse Document Frequency)")

        fig.tight_layout()
        fig.savefig("tfdf_confusion_matrix_anton.png", bbox_inches="tight", dpi=300)

        df.to_csv(output_path)

        titles = self.titles

        self.save_subset_heatmap(df, titles, "castro",  "tfdf_castro_matrix.png")
        self.save_subset_heatmap(df, titles, "marina",  "tfdf_marina_matrix.png")
        self.save_subset_heatmap(df, titles, "mission", "tfdf_mission_matrix.png")

        
    def filter_titles_by_neighborhood(self, titles, neighborhood):
        return [t for t in titles if t.split("_")[2] == neighborhood]

    def save_subset_heatmap(self, df, titles, neighborhood, filename):
        subset_titles = self.filter_titles_by_neighborhood(titles, neighborhood)

        sub_df = df.loc[subset_titles, subset_titles]

        fig, ax = plt.subplots(figsize=(8, 6))
        sn.heatmap(sub_df, ax=ax, cmap="magma", square=True)

        ax.set_title(f"Similarity Matrix — {neighborhood.title()}")
        fig.tight_layout()
        fig.savefig(filename, bbox_inches="tight", dpi=300)
        plt.close(fig)