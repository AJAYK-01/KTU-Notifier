import csv
import pickle
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

def clean_doc(doc):
    # split into tokens by white space
    tokens = doc.split()
    tokens=[w.replace('.','') for w in tokens]
    tokens=[w.replace('-','') for w in tokens]
    tokens=[w.replace('('," ") for w in tokens]
    tokens=[w.replace(')'," ") for w in tokens]
    tokens=[w.replace("'"," ") for w in tokens]
    tokens=[w.lower() for w in tokens]
    tokens = ' '.join(tokens)
    return tokens

def predict_process_docs_cnn(doc):
    documents = list()
    # clean doc
    tokens = clean_doc(doc)
    # add to list
    documents.append(tokens)
    return documents


def predict_cnn(doc):
    predict_docs = predict_process_docs_cnn(doc)

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    encoded_docs = tokenizer.texts_to_sequences(predict_docs)

    X = pad_sequences(encoded_docs, maxlen=94, padding='post')
    # load model
    model = keras.models.load_model('relevancy_model_v2.0.1.h5')
    y=model.predict_classes(np.array(X))
    if (y == [[1]]) :
        #print("\nRelevant \n")
        return(1)
    else :
        #print("\nIrrelevant \n")   
        return(0)



def predict_process_docs_rnn(doc):
    documents = list()
    # clean doc
    tokens = clean_doc(doc)
    # add to list
    documents.append(tokens)
    return documents


def predict_rnn(notif):
    predict_docs = predict_process_docs_rnn(notif)
    max_length=300
    with open('tokenizer_rnn.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    X = tokenizer.texts_to_sequences(predict_docs)
    padding_type = "post"
    trunction_type="post"
    X = pad_sequences(X,maxlen=max_length, padding=padding_type, 
                       truncating=trunction_type)
    # load model
    model = keras.models.load_model('relevancy_model_v3.0.1.h5')
    y=model.predict_classes(X)
    if (y == [[1]]) :
        #print("\nRelevant \n")
        return(1)
    else :
        #print("\nIrrelevant \n")   
        return(0)


def main():
    cnn=0
    rnn=0
    with open('testdatafinal.csv','r') as file:
        reader = csv.reader(file)
        for j,row in enumerate(reader):
            cnn_pred=predict_cnn(row[0])
            if(int(row[1])==cnn_pred):
                cnn=cnn+1
            rnn_pred=predict_rnn(row[0])
            if(int(row[1])==rnn_pred):
                rnn=rnn+1

    print("cnn:",cnn)
    print("rnn:",rnn)

            

if __name__ == "__main__":
    main()