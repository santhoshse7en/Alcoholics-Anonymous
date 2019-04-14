from selenium.webdriver.chrome.options import Options # Options in web browser
from selenium import webdriver # web-based automation tool for Python
from newsplease import NewsPlease # An integrated web crawler and information extractor for news
from bs4 import BeautifulSoup # Python library for pulling data out of HTML and XML files
from requests import get # standard for making HTTP requests in Python
import pandas as pd # library written for data manipulation and analysis
import sys #  System-specific parameters and functions
import time

url= 'https://www.deccanchronicle.com/google-search?q=Alcoholic%20Anonymous'
options = Options()
options.add_argument("--headless")
options=options
browser = webdriver.Chrome(options=options)
browser.maximize_window()
browser.get(url)
time.sleep(1)

res = browser.page_source
soup = BeautifulSoup(res, 'lxml')
pages = [soup.select('.gsc-cursor-page')[i].text.strip() for i in range(len(soup.select('.gsc-cursor-page')))]

urls = []
try:
    # Iterating the same loop twice. Because It's throws an error it can't reach the google search page numbers and on second time its run smoothly
    for page in pages:
        time.sleep(1)
        page = browser.find_element_by_xpath('//*[@id="___gcse_1"]/div/div/div/div[5]/div[2]/div[1]/div/div[2]/div[11]/div/div['+ str(page) +']').click()
        time.sleep(1)
        res = browser.page_source
        soup = BeautifulSoup(res, 'lxml')
        for i in range(len(soup.select('.gsc-webResult'))):
            urls.append(soup.select('.gsc-webResult')[i].a['href'])
        time.sleep(.5)
except:
    for page in pages:
        time.sleep(1)
        page = browser.find_element_by_xpath('//*[@id="___gcse_1"]/div/div/div/div[5]/div[2]/div[1]/div/div[2]/div[11]/div/div['+ str(page) +']').click()
        time.sleep(1)
        res = browser.page_source
        soup = BeautifulSoup(res, 'lxml')
        for i in range(len(soup.select('.gsc-webResult'))):
            urls.append(soup.select('.gsc-webResult')[i].a['href'])
        time.sleep(.5)

browser.quit()

# In google search search results it store cache url which was in the same tag. To remove duplicates execute below line
urls = list(dict.fromkeys(urls))

headline, time, news, image, authors = [], [], [], [], []

for index, url in enumerate(urls):
    # Parse the url to NewsPlease
    article = NewsPlease.from_url(url)

    try:
        # Extracts the Headlines of News Article related to AA
        headline.append(article.title.strip())
    except:
        headline.append(None)

    try:
        # Extracts the Authors of News Article related to AA
        authors.append(article.authors)
    except:
        authors.append(None)

    try:
        # Extracts the Main_Image_url of News Article related to AA
        image.append(article.image_url)
    except:
        image.append(None)

    try:
        # Extracts the Published_Date of News Article related to AA
        time.append(str(article.date_publish.isoformat()))
    except:
        time.append(None)

    try:
        # Extracts the Main_News from Article related to AA
        news.append(article.text.replace('\n', '').replace('\r', '').strip())
    except:
        news.append(None)

    # flush the python output
    sys.stdout.write('\r' + str(index) + ' : ' + str(url) + '\r')
    sys.stdout.flush()

tbl = pd.DataFrame({'Headline' : headline,
                    'Authors' : authors,
                    'Main_Image' : image,
                    'Published_Date' : time,
                    'News' : news,
                    'Source_urls' : urls})
tbl.to_csv('Deccan_Chronicles_AA_News_DETAILS.csv', index=False)
