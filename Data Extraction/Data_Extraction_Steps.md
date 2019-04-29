# Data Extraction methods used for India's Top Newspapers

## Targeted Newspapers are

- The Tribune
- BBC
- Deccan Chronicle
- The Economic Times
- India Today
- Mumbai Mirrors
- Hindustan Times

### Data Extraction parameters as follows
- Headline
- Description
- Author
- Published Date
- News
- URL
- Keywords
- Summary

## Getting Started

### Python Dependencies

```bash
$ pip install selenium
$ pip install beautifulsoup4
$ pip install newspaper3k
$ pip install pandas
```

### Code has been divided into Three section

  * URL Extraction
  * Article details Extraction
  * Creating Data Frame

***First part of the code is mostly on URL's extraction follows similar method with help of [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) & [Selenium](https://selenium-python.readthedocs.io/)***

- Google Custom Keyword Searching

  ```bash
  'Alcoholics Anonymous site: "name of the website"'
  ```

- Finding total number of Google Search Results

   ```python3
   keyword = 'Alcoholics Anonymous site:www.bbc.co.uk'

   url = 'https://www.google.com/search?q=' + '+'.join(keyword.split())

   soup = BeautifulSoup(get(url).text, 'lxml')
   try:
       # Extracts the digits if it the resulted number without comma ','. eg: About 680 results (0.23 seconds)
       max_pages = round([int(s) for s in soup.select_one('div#resultStats').text.split() if s.isdigit()][0]/10)
       max_pages = max_pages + 1
   except:
       # Extracts the digits if it the resulted number without comma ','. eg: About 1,080 results (0.23 seconds)
       max_pages = round(int(''.join(i for i in soup.select_one('div#resultStats').text if i.isdigit()))/10)
       max_pages = max_pages + 1
   ```


- Scraping the resulted urls by iterating the max_pages through while loop  

  ```python3
  options = Options()
  options.headless = True
  browser = webdriver.Chrome(options=options)
  browser.get(url)

  index = 0

  while True:
      try:
          index +=1
          page = browser.page_source
          soup = BeautifulSoup(page, 'lxml')
          linky = [soup.select('.r')[i].a['href'] for i in range(len(soup.select('.r')))]
          urls.extend(linky)
          if index == max_pages:
              break
          browser.find_element_by_xpath('//*[@id="pnnext"]/span[2]').click()
          time.sleep(2)
          sys.stdout.write('\r' + str(index) + ' : ' + str(max_pages) + '\r')
          sys.stdout.flush()
      except:
          pass

  browser.quit()
  ```

***Second part of the code is mostly on extraction of News Articles details & basic NLP stuff regards Keywords in the articles and Summary of the article with the help of [NewsPaper3K](https://pypi.org/project/newspaper3k/)***

- Scraping the news article details by iterating the urls through the for loop

    ```python3
    for index, url in enumerate(urls):
        try:
            # Parse the url to NewsPlease
            soup = BeautifulSoup(get(url).text, 'lxml')
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            # Extracts the Headlines
            try:
                try:
                    headlines.append(article.title.strip())
                except:
                    headlines.append(soup.select_one('meta[property="og:title"]')['content'].strip())
            except:
                headlines.append(None)

            # Extracts the Descriptions    
            try:
                try:
                    descriptions.append(soup.select_one('meta[property="og:description"]')['content'].strip().replace('\n', ' '))
                except:
                    descriptions.append(article.meta_description.strip())
            except:
                descriptions.append(None)

            # Extracts the Authors
            try:
                try:
                    authors.append(soup.select_one('meta[name="author"]')['content'].strip())
                except:
                    authors.append(article.authors.strip())
            except:
                authors.append(None)

            # Extracts the published dates
            try:
                try:
                    dates.append(soup.select_one('meta[property="article:published_time"]')['content'].strip())
                except:
                    dates.append(str(article.publish_date))
            except:
                dates.append(None)

            # Extracts the news articles
            try:
                try:
                    news.append(soup.select_one('.storyText').text.replace('\n', '').strip())
                except:
                    news.append(article.text.strip())
            except:
                news.append(None)

            # Extracts Keywords and Summaries    
            try:
                keywords.append(article.keywords)
                summaries.append(article.summary)
            except:
                keywords.append(None)
                summaries.append(None)

        except:
            headlines.append(None)
            descriptions.append(None)
            authors.append(None)
            dates.append(None)
            news.append(None)
            keywords.append(None)
            summaries.append(None)

        sys.stdout.write('\r' + str(index) + ' : ' + str(url) + '\r')
        sys.stdout.flush()
    ```

***Final Step***

- From the collected data creating the [Pandas](https://pypi.org/project/pandas/) DataFrame and droping the Nan values

    ```python3
    tbl = pd.DataFrame({'Headlines' : headlines,
                    'Descriptions' : descriptions,
                    'Authors' : authors,
                    'Published_Dates' : dates,
                    'Articles' : news,
                    'Keywords' : keywords,
                    'Summaries' : summaries,
                    'Source_URLs' : urls})

    tbl.dropna()
    tbl.to_csv('BBC.csv', index=False)
    ```
