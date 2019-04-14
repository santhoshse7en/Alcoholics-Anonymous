from newsplease import NewsPlease # An integrated web crawler and information extractor for news
from bs4 import BeautifulSoup # Python library for pulling data out of HTML and XML files
from requests import get # standard for making HTTP requests in Python
import pandas as pd # library written for data manipulation and analysis
import sys #  System-specific parameters and functions

df = pd.read_csv('urls.csv')

headline, time, news, image, authors = [], [], [], [], []

for index, url in enumerate(df['urls']):
    try:
        # Parse the url to NewsPlease
        article = NewsPlease.from_url(url)

        # Extracts the Headlines of News Article related to AA
        headline.append(article.title.strip())

        # Extracts the Authors of News Article related to AA
        authors.append(article.authors)

        # Extracts the Main_Image_url of News Article related to AA
        image.append(article.image_url)

        # Extracts the Published_Date of News Article related to AA
        time.append(str(article.date_publish.isoformat()))

        # Extracts the Main_News from Article related to AA
        news.append(article.text.replace('\n', '').replace('\r', '').strip())
    except:
        headline.append(None)
        authors.append(None)
        image.append(None)
        time.append(None)
        news.append(None)

    sys.stdout.write('\r' + str(index) + ' : ' + str(url) + '\r')
    sys.stdout.flush()

tbl = pd.DataFrame({'Headline' : headline,
                    'Authors' : authors,
                    'Main_Image' : image,
                    'Published_Date' : time,
                    'News' : news,
                    'Source_urls' : df['urls']})
tbl.to_csv('Economics_Times_AA_News_DETAILS.csv', index=False)
