import pandas as pd
import numpy as np
import csv
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import xgboost


# Read The data
training_set = pd.read_json('processed_data/train_set.json')
test_set = pd.read_json('processed_data/test_set.json')

roberta_train = pd.read_csv("processed_data/roberta_train.csv")[["label"]]
roberta_test = pd.read_csv("processed_data/roberta_test.csv")[["label"]]
roberta_train.rename(columns={"label": "roberta"},inplace=True)
roberta_test.rename(columns={"label": "roberta"},inplace=True)

gltr_train = pd.read_csv("processed_data/gltr_train.csv")
gltr_test = pd.read_csv("processed_data/gltr_test.csv")

keywords_train = pd.read_csv("processed_data/keywords_train.csv")
keywords_test = pd.read_csv("processed_data/keywords_test.csv")

embedding_train = pd.read_csv("processed_data/embedding_train.csv")
embedding_test = pd.read_csv("processed_data/embedding_test.csv")

ngrams_train = pd.read_csv("processed_data/ngrams_train.csv")
ngrams_test = pd.read_csv("processed_data/ngrams_test.csv")

rouge_train = pd.read_csv("processed_data/rouge_train.csv")
rouge_test = pd.read_csv("processed_data/rouge_test.csv")

# Combining
X = pd.concat([roberta_train, gltr_train, keywords_train, embedding_train, ngrams_train, rouge_train], axis = 1)
Y = training_set.label
#X_train, X_val , Y_train, Y_val = train_test_split(X, Y, test_size=0.02, random_state=0)

with open('processed_data/xgboost_tuned_params.txt', 'r') as file:
    params = eval(file.read())


# Classifier
dtrain = xgboost.DMatrix(X, label = Y)

best_model = xgboost.train(
    params,
    dtrain,
    num_boost_round=45
)

'''
xgbc = XGBClassifier(objective='binary:logistic', colsample_bytree= 0.7, learning_rate= 0.1, max_depth= 2, n_estimators= 100, use_label_encoder=False, eval_metric='error')
clf = xgbc.fit(X_train, Y_train)
'''
'''
y_pred_val = xgbc.predict(X_val)
y_pred_val = y_pred_val.round(0).astype(int)
'''

'''
print("Accuracy :", accuracy_score(Y_val, y_pred_val))
print("Accuracy without features", accuracy_score(Y_val, np.round(X_val[["roberta"]].to_numpy(),0)))
'''
# Write predictions to a file
X_test = pd.concat([roberta_test, gltr_test, keywords_test, embedding_test, ngrams_test, rouge_test], axis = 1)

#predictions = xgbc.predict(X_test)
dtest = xgboost.DMatrix(X_test)
predictions = best_model.predict(dtest)
predictions = predictions.round(0).astype(int)

with open("output/output/submission.csv", "w") as pred:
    csv_out = csv.writer(pred)
    csv_out.writerow(['id','label'])
    for i, row in enumerate(predictions):
        csv_out.writerow([i, row])