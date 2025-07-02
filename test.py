import requests
from bs4 import BeautifulSoup

url = 'https://www.foxnews.com/politics/schumer-force-senate-reading-trumps-entire-big-beautiful-bill'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers, timeout=10)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = '\n'.join([p.get_text() for p in paragraphs])
    print(article_text)
    print(len(article_text))
else:
    print(f"Request failed with status code {response.status_code}")
