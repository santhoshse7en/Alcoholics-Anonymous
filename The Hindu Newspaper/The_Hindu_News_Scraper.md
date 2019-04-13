# The Hindu News Scraper

The Hindu is an Indian daily newspaper, headquartered in Chennai. It was started as a weekly in 1878 and became a daily in 1889. The Hindu is the ninth-most-circulated newspaper in India. So, It's a good start for data extraction of Alcoholic Anonymous related articles. 

**Average Alcoholic Anonymous News and Meetings articles in The Hindu (~ 11,800). Alcoholic Anonymous Meetings Schedule articles are approximately (~ 10,600)**

This python script to find the total number of articles published in The Hindu Newspaper and total number of pages

```python 
from bs4 import BeautifulSoup # Python library for pulling data out of HTML and XML files
from requests import get # standard for making HTTP requests in Python

url = 'https://www.thehindu.com/search/?q=Alcoholics%20Anonymous&order=DESC&sort=publishdate&page=1'
response = get(url)
soup = BeautifulSoup(response.text, 'lxml')

# for collecting the total number of article
article_count = int(''.join(i for i in soup.select_one('.section-controls').span.text.split('of')[1] if i.isdigit()))

# to find the no.of pages
max_pages = int(article_count)//12
```
## Scraping the News Article with help of [news-please](https://github.com/fhamborg/news-please) an integrated web crawler and information extractor for news.

**Author** [Felix Hamborg](https://github.com/fhamborg)

news-please is an open source, easy-to-use news crawler that extracts structured information from almost any news website. It can follow recursively internal hyperlinks and read RSS feeds to fetch both most recent and also old, archived articles. You only need to provide the root URL of the news website to crawl it completely. news-please combines the power of multiple state-of-the-art libraries and tools, such as scrapy, Newspaper, and readability. news-please also features a library mode, which allows Python developers to use the crawling and extraction functionality within their own program. Moreover, news-please allows to conveniently crawl and extract articles from commoncrawl.org.

**Extracted information**
- headline
- lead paragraph
- main content (textual)
- main image
- author's name
- publication date
- language

## Installation

We prefer Python 3, but Python 2.7 is supported, too!
```bash
$ pip3 install news-please 
```
