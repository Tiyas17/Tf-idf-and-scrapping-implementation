import os
import pickle

data_path = "Data/QData"
num_ques = 2405

# split line into words, remove punctuation, convert to lowercase, remove not alphanumeric characters
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

# Create a vocab of all words
# TODO: Can we do anything about non-meaningful words?
vocab = {}
documents = []    # list of list of processed words for each document
for index in range(1, num_ques+1):
    file_path = os.path.join(data_path, str(index) + ".txt")
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        tokens = []  # all words in the document
        for line in lines:
            words = process_line(line)
            tokens += words # merge 2 lists
            
        documents.append(tokens) 
        tokens = set(tokens)     # removing duplicates will help in calculating idf
        for token in tokens:
            if(token == ""):
                continue
            if token not in vocab:
                vocab[token] = 1
            else:
                vocab[token] += 1   
    else:
        print(f"File {index} does not exist")
     
# reverse sort vocab by idf
vocab = {k: v for k, v in sorted(vocab.items(), key=lambda item: item[1], reverse=True)}
        
print("Vocab created")
print("Size of vocab:", len(vocab))
print("Size of documents:", len(documents))
# print(vocab)
            
# Save the vocab in a text file
with open("Data/vocab.txt", 'w', encoding='utf-8') as file:
    for word in vocab:
        file.write(f"{word} {vocab[word]}\n")

# Save the vocab in a pickle file
with open("Data/vocab.pkl", 'wb') as file:
    pickle.dump(vocab, file)
    
# Save the documents in a pickle file
with open("Data/documents.pkl", 'wb') as file:
    pickle.dump(documents, file)
    

# Creare inverted_index to store the docs vocab words are present in 
inverted_index = {}   # key: word, value: list of doc ids
for ind, doc in enumerate(documents):
    ind+=1     # 0-based index
    words = set(doc)
    for word in words:
            if word not in inverted_index:
                inverted_index[word] = [ind]
            else:
                inverted_index[word].append(ind)
            # break
                
print("Inverted index created")
print("Size of inverted index:", len(inverted_index))
# print(inverted_index)

# save inverted index
with open("Data/inverted_index.txt", 'w', encoding='utf-8') as file:
    for word in inverted_index:
        file.write(f"{word}\t{inverted_index[word]}\n")
        
# save inverted index in a pickle file
with open("Data/inverted_index.pkl", 'wb') as file:
    pickle.dump(inverted_index, file)
        
        

