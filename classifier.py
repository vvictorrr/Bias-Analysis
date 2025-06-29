from newsapi import NewsApiClient
from newspaper import Article
from datetime import datetime, timedelta

current_date = str(datetime.today().date())
print(current_date)
lastmonth_date = str((datetime.today() - timedelta(days=30)).date())
print(lastmonth_date)

keywords = ['abortion', 'trump', 'violence', 'protest', 'immigraton',
            'gun control', 'election', 'war', 'israel', 'corrupt']
# Init
newsapi = NewsApiClient(api_key='***REMOVED***')

# /v2/everything
for keyword in keywords:
    all_articles = newsapi.get_everything(q='trump',
                                        from_param=current_date,
                                        to=lastmonth_date,
                                        language='en',
                                        sort_by='relevancy',
                                        page=1)
    top100 = all_articles['articles'][:100]
    for i in top100:
        print(i['source']['name'])
        article = Article(i['url'])
        article.download()
        article.parse()
        print(article.text)

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