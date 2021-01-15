import time
from contextlib import contextmanager
import pandas as pd
import numpy as np
from selenium import webdriver  # Selenium imports
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException
@contextmanager
def timer(title):
    t0 = time.time()
    yield
    print("{} - done in {:.0f}s".format(title, time.time() - t0))
def init_driver(path):  # path = 'chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-plugins-discovery')
    # chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(executable_path=path, options=chrome_options)
    return browser

def book_scrape(num_books: int):
    df_url = pd.read_csv('just_for_links.csv', usecols=['Title_URL'])
    url_list = df_url['Title_URL'].tolist()
    books = []
    browser = init_driver(path='chromedriver.exe')  # location of chromedriver.exe
    for link in url_list[0 : num_books]:
        browser.get(link)
        try:  # BOOK TITLE
            book_name = browser.find_element_by_xpath('.//div[@class="last col stacked"]//div[@class="last col"]//following-sibling::*').text
        except NoSuchElementException:
            book_name = np.nan
        try:  # AUTHOR
            author = browser.find_element_by_xpath('.//div[@class="last col stacked"]//div[@class="last col"]//div[@id="bookAuthors"]//span[@itemprop="author"]//div[@class="authorName__container"]//following-sibling::*').text
        except NoSuchElementException:
            author = np.nan
        try:  # RATINGS of book
            rating = browser.find_element_by_xpath('.//div[@class="uitext stacked"]//span[@itemprop="ratingValue"]').text
        except NoSuchElementException:
            rating = np.nan
        try:  # NUMBR OF RATINGS
            num_rating = browser.find_element_by_xpath('.//div[@class="uitext stacked"]//a[@class="gr-hyperlink"]').text
        except NoSuchElementException:
            num_rating = np.nan
        try:  # NUMBER OF REVIEWS
            num_reviews = browser.find_element_by_xpath('//*[@id="bookMeta"]/a[3]').text
        except NoSuchElementException:
            num_reviews = np.nan
        try:  # PAGES
            pages = browser.find_element_by_xpath('//*[@id="details"]/div[1]/span[3]').text
        except NoSuchElementException:
            pages = np.nan
        try:  # PUBLISH YEAR (have to clean)
            publish_year = browser.find_element_by_xpath('//*[@id="details"]/div[2]').text
        except NoSuchElementException:
            publish_year = np.nan
        try:  # CLICK ON MORE DETAILS
            browser.find_element_by_xpath('.//div[@class="buttons"]//a[text()="More Details..."]').click()
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
            pass
        try:  # URL of BOOK
            url = browser.find_element_by_xpath('//*[@id="bookDataBox"]/div[3]/div[2]/a').text
        except NoSuchElementException:
            url = np.nan
        try:   # SERIES
            series = browser.find_element_by_xpath('//*[@id="bookDataBox"]/div[4]/div[2]/a').text
            # print(series)
        except NoSuchElementException:
            series = np.nan
        try:  # AWARDS
            awards = browser.find_element_by_xpath('//*[@id="bookDataBox"]/div[8]/div[2]').text
        except NoSuchElementException:
            awards = np.nan
        try:  # PLACES
            places = browser.find_element_by_xpath('//*[@id="bookDataBox"]/div[7]').text
        except NoSuchElementException:
            places = np.nan
        try:  # GENRE 1
            genre_1 = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[5]/div[7]/div/div[2]/div/div[1]/div[1]/a').text
        except NoSuchElementException:
            genre_1 = np.nan
        try:  # GENRE 2
            genre_2 = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[5]/div[7]/div/div[2]/div/div[2]/div[1]/a').text
        except NoSuchElementException:
            genre_2 = np.nan
        try:   # GENRE 3
            genre_3 = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[5]/div[7]/div/div[2]/div/div[3]/div[1]/a').text
        except NoSuchElementException:
            genre_3 = np.nan
        books.append({'Title': book_name, "author": author, "rating": rating, "num_rating": num_rating, "num_reviews": num_reviews,
                      "pages": pages, "publish_year": publish_year, "url": url, "series": series, "awards": awards, "places": places,
                      "genre_1": genre_1, "genre_2": genre_2, "genre_3": genre_3})
    browser.quit()
    print(f"Scrapped data of {len(books)} books.")
    df = pd.DataFrame(books)
    df.to_csv("books_2000.csv")
    return df
if __name__=='__main__':
    with timer("Start Scrapping"):
        df = book_scrape(num_books=10)


