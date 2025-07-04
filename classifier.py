from newsapi import NewsApiClient
from newspaper import Article
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import requests


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

#source bias
source_bias = {
    'Fox News': 'right',
    'The Daily Caller': 'right',
    'Breitbart News': 'right',
    'Newsmax': 'right',
    'New York Post': 'lean right',
    'Forbes': 'center',
    'BBC News': 'center',
    'Reuters': 'center',
    'NPR': 'center',
    'Business Insider': 'center',
    'DW (English)': 'center',
    'Yahoo Entertainment': 'lean left',
    'The Verge': 'lean left',
    'Gizmodo': 'lean left',
    'CNN': 'lean left',
    'ABC News': 'lean left',
    'The Associated Press': 'center',
    'Time': 'lean left',
    'Gizmodo.com': 'lean left',
    'NBC News': 'lean left',
    'Al Jazeera English': 'lean left',
    'Slate Magazine': 'left',
    'Wired': 'left',
    'Jezebel': 'left',
    'MSNBC': 'left',
    'HuffPost': 'left',
    'The Guardian': 'left',
    'The Atlantic': 'left',
    'The New Yorker': 'left',
    'The New Yorker': 'left',
    'Vox': 'left',
    'Rolling Stone': 'left'
}

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



'''
for keyword in keywords:
    all_articles = newsapi.get_everything(q=keyword,
                                        from_param=current_date,
                                        to=lastmonth_date,
                                        language='en',
                                        sort_by='relevancy',
                                        page=1)
    top100 = all_articles['articles'][:100]
    for i in top100:
        joo.append(i['source']['name'])

boo = {}
for source in joo:
    if source in boo:
        boo[source] += 1
    else:
        boo[source] = 1

print(boo)'''
#for keyword in keywords:
#    all_articles = newsapi.get_everything(q='trump',
#                                        from_param=current_date,
#                                        to=lastmonth_date,
#                                        language='en',
#                                        sort_by='relevancy',
#                                        page=1)
#    top100 = all_articles['articles'][:100]
#    for i in top100:
#        print(i['source']['name'])
#        article = Article(i['url'])
#        article.download()
#        article.parse()
#        print(article.text)

# /v2/top-headlines/sources
#sources = newsapi.get_sources()
#top100 = all_articles['articles'][:100]
#
#for i in top100:
#    print(i['source']['name'])
#    article = Article(i['url'])
#    article.download()
#    article.parse()
#    print(article.text)
#print(top100)


#url = 'https://www.bbc.com/news/articles/cqx28yr8gj1o'
#article = Article(url)
#article.download()
#article.parse()
#print("**Main Text:**", article.text)

#for i in top100:
#    print(i['source']['name'])
#    article = Article(i['url'])
#    article.download()
#    article.parse()
#    print(article.text)
#for i in top_headlines['articles']:
#    print('Source:', i['source']['id'])
#    print(i['content'])
#    print('-------')
