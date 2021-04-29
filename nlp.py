from os import listdir
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, Bidirectional
from sklearn.model_selection import train_test_split
import numpy as np
import pickle

# load doc into memory
def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text


# pre processing
def clean_doc(doc):
    tokens = doc.split()
    #removing unnecessary characters
    tokens=[w.replace('.','') for w in tokens]
    tokens=[w.replace('-','') for w in tokens]
    tokens=[w.replace('('," ") for w in tokens]
    tokens=[w.replace(')'," ") for w in tokens]
    tokens=[w.replace("'","") for w in tokens]
    tokens=[w.replace('"',"") for w in tokens]
    tokens=[w.lower() for w in tokens]
    #return as a string 
    tokens = ' '.join(tokens)
    return tokens




def process_docs(directory, is_trian):
    documents = list()
    print(directory+" : ",len(listdir(directory)))
    # walk through all files in the folder
    for filename in listdir(directory):
        # create the full path of the file to open
        path = directory + '/' + filename
        # load the doc
        doc = load_doc(path)
        # clean doc
        tokens = clean_doc(doc)
        # add to list
        documents.append(tokens)
        
    return documents


def make_model():
    # load all notifications
    positive_docs = process_docs('data/pos_train', True)
    negative_docs = process_docs('data/neg_train', True)

    X = negative_docs + positive_docs

    y = np.array([0 for _ in range(270)] + [1 for _ in range(270)])

    #Train Test Spliting data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    #Parameters to embed words to matrices
    vocab_size = 1000
    oov_token = "<OOV>"
    max_length = 300
    padding_type = "post"
    trunction_type="post"
    
    #Creating a Tokenizer from Train Set
    tokenizer = Tokenizer(num_words = vocab_size,oov_token=oov_token)
    tokenizer.fit_on_texts(X_train)
    #Saving the Tokenizer for Prediction
    with open('tokenizer_rnn.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #mapping tokenizer
    word_index = tokenizer.word_index

    #Converting Train and Test Notifications to matrices by tokenizing
    X_train_sequences = tokenizer.texts_to_sequences(X_train)
    X_train_padded = pad_sequences(X_train_sequences,maxlen=max_length, padding=padding_type, 
                       truncating=trunction_type)
    X_test_sequences = tokenizer.texts_to_sequences(X_test)
    X_test_padded = pad_sequences(X_test_sequences,maxlen=max_length, 
                               padding=padding_type, truncating=trunction_type)


    embeddings_index = {}

    #Download glove beforehand
    f = open('glove.6B/glove.6B.100d.txt')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()

    #Creating embedding matrix for each word in Our corpus
    embedding_matrix = np.zeros((len(word_index) + 1, 100))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector

    #Defining Embedding layer
    embedding_layer = Embedding(len(word_index) + 1,
                                100,
                                weights=[embedding_matrix],
                                input_length=max_length,
                                trainable=False)
                    
    embedding_dim = 16
    input_length = 300


    #Model Architecture
    model = Sequential([
        embedding_layer,
        Bidirectional(LSTM(embedding_dim, return_sequences=True)),
        Bidirectional(LSTM(embedding_dim,)),
        Dense(6, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    print(model.summary())

    model.fit(X_train_padded, y_train, epochs=10, validation_data=(X_test_padded, y_test))
    
    #Saving Model for prediction
    model.save("relevancy_model_v3.0.1.h5")


def predict_process_docs(doc):
    documents = list()
    # clean doc
    tokens = clean_doc(doc)
    # add to list
    documents.append(tokens)
    return documents


def relevant(notif):
    predict_docs = predict_process_docs(notif)
    max_length=300
    with open('tokenizer_rnn.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    X = tokenizer.texts_to_sequences(predict_docs)
    padding_type = "post"
    trunction_type="post"
    X = pad_sequences(X,maxlen=max_length, padding=padding_type, 
                       truncating=trunction_type)
    # load model
    model = keras.models.load_model('relevancy_model.h5')
    y=model.predict_classes(X)
    if (y == [[1]]) :
        #print("\nRelevant \n")
        return(1)
    else :
        #print("\nIrrelevant \n")   
        return(0)



if __name__ == "__main__":
    print(predict("Webinar for S3 students on Quantum Computing on 26/11/2021"))