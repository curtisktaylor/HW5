!pip install spacy
!pip install newsapi-python
!python -m spacy download en_core_web_lg

import spacy
import pandas as pd
import pickle
from newsapi import NewsApiClient
from string import punctuation
from collections import Counter

dados = []
titles = []
dates = []
descriptions = []

nlp_eng = spacy.load("en_core_web_lg")
newsapi = NewsApiClient (api_key='xxxxxxxx')

articles = []
results = []

for i in range(5):
  temp = newsapi.get_everything(q='coronavirus', language='en', from_param='2022-03-27', to='2022-02-27', sort_by='relevancy', page=(i + 1))
  articles.append(temp)

filename = 'articlesCOVID.pckl'
pickle.dump(articles, open(filename, 'wb'))

for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        date = x['publishedAt']
        description = x['description']
        content = x['content']
        dados.append({'title':title, 'date':date, 'desc':description, 'content':content})
df = pd.DataFrame(dados)
df = df.dropna()
df.head()


for content in df.content.values:
    results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])

df['keywords'] = results



def get_keywords_eng(text):
  result = []
  pos_tag = ['PROPN', 'VERB', 'NOUN']
  doc = nlp_eng(text.lower())
  for token in doc:
    if (token.text in nlp_eng.Defaults.stop_words or token.text in punctuation):
      continue
    if (token.pos_ in pos_tag):
      result.append(token.text)
  return result
  
