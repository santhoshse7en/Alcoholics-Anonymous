# The Hindu News Scraper

The Hindu is an Indian daily newspaper, headquartered in Chennai. It was started as a weekly in 1878 and became a daily in 1889. The Hindu is the ninth-most-circulated newspaper in India. So, It's a good start for data extraction of Alcoholic Anonymous related articles.

**Average Alcoholic Anonymous News and Meetings articles in The Hindu (~ 11,842). Alcoholic Anonymous Meetings Schedule articles are approximately (~ 11,191)**

## Getting Started 

### Python Dependencies
We prefer Python 3, but Python 2.7 is supported, too!
```bash
$ pip install beautifulsoup4
$ pip install pandas
```

### Code has been divided into Three section 

  * URL Extraction
  * Article details Extraction
  * Creating DataFrame


***First part of the code is mostly on urls extraction and basic details of articles follows similar method with help of [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)***
- Finding total number of pages from total number of articles
    ```python3
    from bs4 import BeautifulSoup # Python library for pulling data out of HTML and XML files
    from requests import get # standard for making HTTP requests in Python

    url = 'https://www.thehindu.com/search/?q=Alcoholics%20Anonymous&order=DESC&sort=publishdate'
    soup = BeautifulSoup(get(url).text, 'lxml')

    # for collecting the total number of article
    article_count = int(''.join(i for i in soup.select_one('.section-controls').span.text.split('of')[1] if i.isdigit()))

    # to find the no.of pages
    max_pages = int((int(article_count)//12) + 2)
    
    for index, i in enumerate(range(1, max_pages)):    
      url = 'https://www.thehindu.com/search/?q=Alcoholic%20Anonymous&order=DESC&sort=publishdate&page=' + str(i)
      soup = BeautifulSoup(get(url).text, 'lxml')

      # Extracts url's 
      url = [soup.select('a.story-card75x1-text')[i]['href'] for i in range(len(soup.select('a.story-card75x1-text')))]
      urls.extend(url)

      # Extracts headline's
      headline = [soup.select('.story-card75x1-text')[i].text.strip() for i in range(len(soup.select('.section-name')))]
      headlines.extend(headline)

      # Extracts author's 
      for i in range(len(soup.select('.story-card-news'))):
          try:
              authors.append(soup.select('.story-card-news')[i].select_one('.story-card-33-author-name').text.strip())
          except:
              authors.append(None)

      # Extracts Date's
      date = [soup.select('.dateline')[i].text.strip() for i in range(len(soup.select('.dateline')))]
      dates.extend(date)

      sys.stdout.write('\r' + str(index) + ' : ' + str(max_pages))
      sys.stdout.flush()
    ```
    
***Second part of the code is mostly on extraction of News Articles details with the help of [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)***
- Scraping the news article details by iterating the urls through the for loop
    ```python3
    for index, url in enumerate(urls):
      try:
          # Parse the url to NewsPlease 
          soup = BeautifulSoup(get(url).text, 'lxml')

          try:
              # Extracts the Descriptions
              desc = soup.select_one('meta[name="description"]')['content'].strip().replace('\n', ' ')
              descriptions.append(desc)
          except:
              descriptions.append(None)

          try:
              # Extracts the news articles
              para = soup.select_one('.article').select('p')
              text = ''.join(str(e.text.strip().replace('\n', '').replace("[^a-zA-Z]", " ")) for e in para)
              news.append(text)
          except:
              news.append(None)

      except:
          descriptions.append(None)
          news.append(None)

      sys.stdout.write('\r' + str(index) + ' : ' + str(url) + '\r')
      sys.stdout.flush()
    ```

***Final Step***

- From the collected data creating the [Pandas](https://pypi.org/project/pandas/) DataFrame

    ```python3
    tbl = pd.DataFrame({'Headlines' : headlines,
                    'Descriptions' : descriptions,
                    'Authors' : authors,
                    'Published_Dates' : dates,
                    'Articles' : news})

    tbl.to_csv('The_Hindu.csv', index=False)
    ```
