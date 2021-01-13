import time
import pandas as pd
import numpy as np
# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def init_driver(path):  # path = 'chromedriver.exe'
    # Initialize chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--disable-plugins-discovery')
    # chrome_options.add_argument('--start-maximized')
    browser = webdriver.Chrome(executable_path=path, options=chrome_options)
    return browser


def book_scrape(num_books: int):
    df_url = pd.read_csv('just_for_links.csv', usecols='Title_URL')
    url_list = df_url['Title_URL'].tolist()
    books = []
    browser = init_driver(path='chromedriver.exe')  # location of chromedriver.exe
    for link in url_list[0 : num_books]:
        browser.get(link)
        time.sleep(2)
        try:
            browser.find_element_by_css_selector('[alt="Dismiss"]').click()  # clicking to the X.
            print(' x out .worked')
        except (NoSuchElementException, ElementNotInteractableException):
            # print(' x out failed')
            pass
        time.sleep(1)
        # BOOK TITLE
        try:
            book_name = browser.find_element_by_xpath(
                './/div[@class="last col stacked"]//div[@class="last col"]//following-sibling::*').text
            # print(book_name)
        except NoSuchElementException:
            book_name = np.nan
        # AUTHOR
        try:
            author = browser.find_element_by_xpath(
                './/div[@class="last col stacked"]//div[@class="last col"]//div[@id="bookAuthors"]//span[@itemprop="author"]//div[@class="authorName__container"]//following-sibling::*').text
            # print(author)
        except NoSuchElementException:
            author = np.nan
        # RATINGS of book
        try:
            rating = browser.find_element_by_xpath(
                './/div[@class="uitext stacked"]//span[@itemprop="ratingValue"]').text
            # print(rating)
        except NoSuchElementException:
            rating = np.nan
        # NUMBR OF RATINGS
        try:
            num_rating = browser.find_element_by_xpath('.//div[@class="uitext stacked"]//a[@class="gr-hyperlink"]').text
            # print(num_rating)
        except NoSuchElementException:
            num_rating = np.nan
        # NUMBER OF REVIEWS
        try:
            num_reviews = browser.find_element_by_xpath('//*[@id="bookMeta"]/a[3]').text
            # print(num_reviews)
        except NoSuchElementException:
            num_reviews = np.nan
        # PAGES
        try:
            pages = browser.find_element_by_xpath('//*[@id="details"]/div[1]/span[3]').text
            # print(pages)
        except NoSuchElementException:
            pages = np.nan
        # PUBLISH YEAR (have to clean)
        try:
            publish_year = browser.find_element_by_xpath('//*[@id="details"]/div[2]').text
            # print(publish_year)
        except NoSuchElementException:
            publish_year = np.nan
        # CLICK ON MORE DETAILS
        try:
            browser.find_element_by_xpath('.//div[@class="buttons"]//a[text()="More Details..."]').click()
        except (StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException,
                ElementNotInteractableException):
            pass
        # URL of BOOK
        try:
            url = browser.find_element_by_xpath('//*[@id="bookDataBox"]/div[3]/div[2]/a').text
            # print(url)
        except NoSuchElementException:
            url = np.nan
        # SERIES
        try:
            series = browser.find_element_by_xpath('//*[@id="bookDataBox"]/div[4]/div[2]/a').text
            # print(series)
        except NoSuchElementException:
            series = np.nan
        # AWARDS
        try:
            awards = browser.find_element_by_xpath('//*[@id="bookDataBox"]/div[8]/div[2]').text
            # print(awards)
        except NoSuchElementException:
            awards = np.nan
        # PLACES
        try:
            places = browser.find_element_by_xpath('//*[@id="bookDataBox"]/div[7]').text
            # print(places)
        except NoSuchElementException:
            places = np.nan
        # GENRE 1
        try:
            genre_1 = browser.find_element_by_xpath(
                '/html/body/div[2]/div[3]/div[1]/div[2]/div[5]/div[7]/div/div[2]/div/div[1]/div[1]/a').text
            # print(genre_1)
        except NoSuchElementException:
            genre_1 = np.nan
        # GENRE 2
        try:
            genre_2 = browser.find_element_by_xpath(
                '/html/body/div[2]/div[3]/div[1]/div[2]/div[5]/div[7]/div/div[2]/div/div[2]/div[1]/a').text
            # print(genre_2)
        except NoSuchElementException:
            genre_2 = np.nan
        # GENRE 3
        try:
            genre_3 = browser.find_element_by_xpath(
                '/html/body/div[2]/div[3]/div[1]/div[2]/div[5]/div[7]/div/div[2]/div/div[3]/div[1]/a').text
            # print(genre_3)
        except NoSuchElementException:
            genre_3 = np.nan
        time.sleep(0.5)

        books.append({'Title': book_name,
                      "author": author,
                      "rating": rating,
                      "num_rating": num_rating,
                      "num_reviews": num_reviews,
                      "pages": pages,
                      "publish_year": publish_year,
                      "url": url,
                      "series": series,
                      "awards": awards,
                      "places": places,
                      "genre_1": genre_1,
                      "genre_2": genre_2,
                      "genre_3": genre_3})
    browser.quit()
    print(f"Scrapped data of {len(books)} books.")
    df = pd.DataFrame(books)
    df.to_csv("books_2000.csv")

    return df
