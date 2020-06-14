import numpy as np 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import string
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import re
import pickle
from utils import stopwords

print(stopwords)

lemmatizer = WordNetLemmatizer()
naive = MultinomialNB()

print('imports done !!')
import os
files = []
for dirname, _, filenames in os.walk(os.getcwd() + '/data'):
    for filename in filenames:
        files.append(os.path.join(dirname, filename))

print('creating data !!')
# creating data.
df = pd.read_csv(files[0])
for i in range(1, len(files)):
    df = pd.concat([df, pd.read_csv(files[i])], axis = 0)

# shuffling the data.
df = np.array(df)
np.random.shuffle(df)
df = pd.DataFrame(data = df, columns = ['news', 'category'])

# preprocessing news.
def preprocess_news(val):
    val = ''.join(re.findall('[A-Za-z\s]', val))
    val = val.lower()
    val = [word for word in val.split() if word not in stopwords]
    val = [lemmatizer.lemmatize(word) for word in val]
    val = ' '.join(val)
    return val

df['processed_news'] = df.news.apply(preprocess_news)
df.drop(['news'], axis = 1, inplace = True)

# creating test data.
split_point = int(df.shape[0] - 0.12*df.shape[0])
train = df[:split_point]
test = df[split_point:]

# model creation and training.

print('model initialised !!')
mapper = {'business' : 1, 'technology' : 2, 'science' : 3, 'sports' : 4, 
          'entertainment' : 5, 'health' : 6}
demapper = {val : key.title() for key, val in mapper.items()}
x, y = train.processed_news, train.category.map(mapper)

vec = TfidfVectorizer()
x = vec.fit_transform(x).toarray()
skf = StratifiedKFold(n_splits = 10, random_state = 101, shuffle = True)

score = []
for i, (train_idx, test_idx) in enumerate(skf.split(x, y)):
    print(f'running fold {i}....')
    x_train, x_test = x[train_idx], x[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    naive.fit(x_train, y_train)
    pred = naive.predict_proba(x_test)
    score_i = roc_auc_score(y_test, pred, multi_class = "ovo")
    print(f'score of fold_{i} : {score_i}')
    score.append(score_i)

print('-'*50)
print('result :')
print(f'mean score : {np.mean(score)} with {np.std(score)} standard deviation')
print('-'*50)

# saving model and all necessary files.
print('saving model...')
model_file = 'newsy_model.pkl'
vec_file = 'newsy_vec.pkl'
demapper_file = 'newsy_demapper.pkl'
pickle.dump(naive, open(model_file, 'wb'))
pickle.dump(vec, open(vec_file, 'wb'))
pickle.dump(demapper, open(demapper_file, 'wb'))
print('DONE !!')