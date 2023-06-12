import math
import os
import pickle

# vocab = {}
# documents = []
# inverted_index = {}

# load files
with open('Data/vocab.pkl', 'rb') as file:
    vocab = pickle.load(file)
with open('Data/inverted_index.pkl', 'rb') as file:
    inverted_index = pickle.load(file)
with open('Data/documents.pkl', 'rb') as file:
    documents = pickle.load(file)

print("Size of loaded vocab:", len(vocab))
print("Size of loaded inverted index:", len(inverted_index))
print("Size of loaded documents:", len(documents))

# to split, remove punctuation, lowercase, remove not alphanumeric chars


def process_line(line):
    words = line.split()
    processed_words = []

    for word in words:
        word = word.strip('.,;:?!')
        word = word.lower()
        word = ''.join(ch for ch in word if ch.isalnum())
        word = word.strip('0123456789')

        if word != "":
            processed_words.append(word)

    return processed_words


'''
TERMS:
    tf(term, doc)
    idf(term)
    tf-idf(term, doc) = tf(term, doc) * idf(term)
    score(doc) = sum(tf-idf(term, doc) for term in query)
'''

# returns a dict containing tf scores of each document for given term
# one which isn't here has 0 tf score
# TODO: Any new term will have 0 tf, so why not preprocess tf for all vocab as well?


def get_tf_dict(term):
    tf_dict = {}
    # using inverted index to only count over docs that actually contain the term
    if term in inverted_index.keys():
        for doc in inverted_index[term]:
            # print("doc", doc)
            tf_dict[doc] = documents[doc-1].count(term)

    # TODO: normalize or not?
    # for doc in tf_dict.keys():
    #     tf_dict[doc] /= float(len(documents[doc-1]))

    return tf_dict

# returns the idf score of given term: (overall uniqueness of term)


def get_idf(term):
    # TODO: idf when term not in vocab?
    if term not in vocab.keys():
        return 1
    idf = float(vocab[term])  # Doubt: if term not in vocab?
    return math.log(len(documents) / idf)

# returns scores (sorted) of each documents for given query


def get_sorted_documents(query):
    terms = process_line(query)
    # print(terms)

    tf_idf_dict = {}   # tf-idf score for each document by simple average over all terms
    for term in terms:
        tf_dict = get_tf_dict(term)
        idf = get_idf(term)
        for ind, doc in enumerate(documents):
            ind += 1   # 0-based index
            tf_idf = 0
            if ind in tf_dict.keys():
                tf_idf = tf_dict[ind] * idf

            if ind not in tf_idf_dict.keys():
                tf_idf_dict[ind] = tf_idf
            else:
                tf_idf_dict[ind] += tf_idf

    for ind in tf_idf_dict.keys():
        tf_idf_dict[ind] /= float(len(documents))

    # reverse sort tf_idf_dict by value
    tf_idf_dict = dict(
        sorted(tf_idf_dict.items(), key=lambda item: item[1], reverse=True))

    return tf_idf_dict


def print_potential_documents(score_dict, num_docs):
    print(f"Printing top {num_docs} result...")
    with open('Data/index.txt', 'r') as file:
        title = file.readlines()

    for i, doc_ind in enumerate(score_dict.keys()):
        # display no result if no document has score > 0
        if(i == 0 and score_dict[doc_ind] == 0):
            print("No result found!")
            break

        if i == num_docs or score_dict[doc_ind] == 0:
            break
        print(
            f"#{i+1} {title[doc_ind-1].strip()}\t: Score={round(score_dict[doc_ind], 5)}")


query = input("Enter your query: ")
sorted_documents = get_sorted_documents(query)   # sorted by score
print_potential_documents(sorted_documents, 25)
