import pandas as pd
import numpy as np
from tqdm import tqdm
import nltk
from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer
import math
import operator
from functools import reduce
from rouge import Rouge

nltk.download('punkt')

# Data
training_set = pd.read_json('processed_data/train_set.json')
test_set = pd.read_json('processed_data/test_set.json')

# Output
column_names = ["wordsSum", "bigramsSum", "trigramsSum", "fourgramsSum", "bleu_score"]
columns_train = np.zeros((len(training_set),len(column_names)))
columns_test = np.zeros((len(test_set),len(column_names)))

# Word tokenizer - alphanumeric only
tokenizer = RegexpTokenizer(r'\w+')

def geometric_mean(precisions):
    return (reduce(operator.mul, precisions)) ** (1.0 / len(precisions))

for step, (to_process, columns) in enumerate([(training_set,columns_train), (test_set,columns_test)]):
    for i in tqdm(range(len(to_process.index))):
        
        # Data
        text_doc = to_process.loc[i]["document"]
        text_sum = to_process.loc[i]["summary"]

        # Tokenized
        tokenized_doc = tokenizer.tokenize(text_doc.lower())
        tokenized_sum = tokenizer.tokenize(text_sum.lower())

        # Words
        wordsDoc = set(tokenized_doc)
        wordsSum = set(tokenized_sum)
        wordsSum = len(wordsDoc.intersection(wordsSum)) / len(wordsDoc)

        # Bigrams
        bigramsDoc = set(ngrams(tokenized_doc, 2))
        bigramsSum = set(ngrams(tokenized_sum, 2))
        bigramsSum = len(bigramsDoc.intersection(bigramsSum)) / len(bigramsDoc)

        # Trigrams
        trigramsDoc = set(ngrams(tokenized_doc, 3))
        trigramsSum = set(ngrams(tokenized_sum, 3))
        trigramsSum = len(trigramsDoc.intersection(trigramsSum)) / len(trigramsDoc)

        # 4grams
        fourgramsDoc = set(ngrams(tokenized_doc, 4))
        fourgramsSum = set(ngrams(tokenized_sum, 4))
        fourgramsSum = len(fourgramsDoc.intersection(fourgramsSum)) / len(fourgramsDoc)
        
        bleu_score = geometric_mean(precisions=[wordsSum, bigramsSum, trigramsSum, fourgramsSum])

        columns[i] = np.array([wordsSum, bigramsSum, trigramsSum, fourgramsSum, bleu_score])
    
    if step==0:
        pd.DataFrame(columns,columns=column_names).to_csv("processed_data/ngrams_train.csv",index=False)
    else:
        pd.DataFrame(columns,columns=column_names).to_csv("processed_data/ngrams_test.csv",index=False)