# Data Extraction methods used for India's Top Newspapers

## Targeted Newspapers are

- The Hindu
- The Tribune
- BBC
- Deccan Chronicle
- The Economic Times
- India Today
- Mumbai Mirrors
- Hindustan Times

## Getting Started

### Python Dependencies
We prefer Python 3, but Python 2.7 is supported, too!
```bash
$ pip install selenium
$ pip install beautifulsoup4
$ pip install newspaper3k
$ pip install pandas
```

### Code has been divided into Three section

  * URL Extraction
  * Article details Extraction
  * Creating DataFrame

***First part of the code is mostly on urls extraction follows similar method with help of [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) & [Selenium](https://selenium-python.readthedocs.io/)***

- Google Custom Keyword Searching

  ```bash
  'Alcoholic Anonymous site:www.tribuneindia.com'
  ```

- Finding total number of Google Search Results

   ```python3
  keyword = 'Alcoholic Anonymous site:www.tribuneindia.com'

  url = 'https://www.google.com/search?q=' + '+'.join(keyword.split())

  options = Options()
  options.headless = True
  browser = webdriver.Chrome(options=options)
  browser.get(url)

  page = browser.page_source
  soup = BeautifulSoup(page, 'lxml')
  max_pages = int(int(soup.select_one('#resultStats').text.split(' ')[1])//10)

   ```

- Scraping the resulted urls by iterating the max_pages through while loop  

    ```python3
    index = 0

    while True:
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

    browser.quit()
    ```

***Second part of the code is mostly on extraction of News Articles details & basic NLP stuff regards Keywords in the articles and Summary of the article with the help of [NewsPaper3K](https://pypi.org/project/newspaper3k/)***

- Scraping the news article details by iterating the urls through the for loop

    ```python3
    for index, url in enumerate(urls):
      try:
          # Parse the url to NewsPlease
          article = Article(url, timeout=4)
          article.download()
          article.parse()

          try:
              # Extracts the Headlines
              headlines.append(article.title)
          except:
              headlines.append(None)

          try:
              # Extracts the Descriptions
              descriptions.append(article.meta_description)
          except:
              descriptions.append(None)

          try:
              # Extracts the Authors
              authors.append(article.authors)
          except:
              authors.append(None)

          try:
              # Extracts the published dates
              dates.append(str(article.publish_date))
          except:
              dates.append(None)

          try:
              # Extracts the news articles
              news.append(article.text)
          except:
              news.append(None)

          try:
              # Extracts Keywords and Summaries
              article.nlp()
              keywords.append(article.keywords)
              summaries.append(article.summary)
          except:
              keywords.append(None)
              summaries.append(None)

          try:
              # Extracts the image urls
              image_urls.append(article.top_image)
          except:
              image_urls.append(None)

      except:
          headlines.append(None)
          descriptions.append(None)
          authors.append(None)
          dates.append(None)
          news.append(None)
          keywords.append(None)
          summaries.append(None)
          image_urls.append(None)


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
                    'Articles' : news,
                    'Keywords' : keywords,
                    'Summaries' : summaries,
                    'Source_URLs' : urls,
                    'Image_URLs' : image_urls})

    tbl.to_csv('The_Tribune.csv', index=False)
    ```
