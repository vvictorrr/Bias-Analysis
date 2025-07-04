from newsapi import NewsApiClient
from newspaper import Article
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import requests

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")


current_date = str(datetime.today().date())
print(current_date)
lastmonth_date = str((datetime.today() - timedelta(days=30)).date())
print(lastmonth_date)

keywords = ['abortion', 'trump', 'violence', 'protest', 'immigraton',
            'gun control', 'election', 'war', 'israel', 'corrupt']
# Init
newsapi = NewsApiClient(api_key=API_KEY)

'''
sources = newsapi.get_sources()
for i in sources['sources']:
    if i['language'] == 'en':
        print(i['id'], i['name'])'''

bias_source = {'right': 'fox-news, breitbart-news, the-american-conservative',
                'right_lean': 'the-washington-times, national-review, financial-post',
                'center': 'the-wall-street-journal, bbc-news, associated-press',
                'left_lean': 'time, business-insider, cnn',
                'left': 'the-huffington-post, msnbc, wired'}
# /v2/everything

dataset = []

for bias in bias_source.keys():
    try:
        all_articles = newsapi.get_everything(from_param=current_date,
                                            to=lastmonth_date,
                                            sources=bias_source[bias],
                                            language='en',
                                            sort_by='publishedAt',
                                            page_size=100,
                                            page=1)
        articles = all_articles['articles'][:200]
        for art in articles:
            url = art['url']
            text = None
            #print(bias)
            #print(art['source']['name'])
            try:
                article = Article(url)
                article.download()
                article.parse()
                text = article.text.strip()
            except Exception as e:
                print(f"newspaper3k failed for: {art['url']}\ntrying BeautifulSoup")
                try:
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
                    }
                    resp = requests.get(url, headers=headers)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        paragraphs = soup.find_all('p')
                        text = '\n'.join([p.get_text() for p in paragraphs]).strip()
                    else:
                        print(f"Fallback failed with status {resp.status_code}")
                except Exception as e2:
                    print(f"Fallback failed for {url}: {e2}")
                    continue
            if text and len(text) >= 200:
                dataset.append({
                    'bias': bias,
                    'text': text
                })
    except Exception as e3:
        print(f"Error fetching from NewsAPI: {e3}")
        continue

df = pd.DataFrame(dataset)
df.to_csv("bias_classification_dataset.csv", index=False)
