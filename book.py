import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from scrapper import book_scrape

def scrape(file_path):  # location of books_2000.csv
    # df = book_scrape(num_books=1200)
     # ========== OR ============
    df = pd.read_csv(file_path)
    return df


def data_clean(df):
    df.drop("Unnamed: 0", axis=1, inplace=True)
    df.drop_duplicates(inplace=True)

    df['num_rating'] = df['num_rating'].astype(str)
    df['num_rating'] = df['num_rating'].apply(lambda x: x.replace(' ratings', ''))
    df['num_rating'] = df['num_rating'].astype(object)

    df['num_reviews'] = df['num_reviews'].astype(str)
    df['num_reviews'] = df['num_reviews'].apply(lambda x: x.replace(' reviews', ''))
    df['num_reviews'] = df['num_reviews'].astype(object)

    df['pages'] = df['pages'].astype(str)
    df['pages'] = df['pages'].apply(lambda x: x.replace(' pages', ''))
    df['pages'] = df['pages'].astype(object)

    df['genre'] = df[df.columns[10:13]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)
    df.drop(['genre_1', 'genre_2', 'genre_3'], axis=1, inplace=True)
    df['genre'] = df['genre'].replace('', 'missing')

    df['series'] = df['series'].astype(str)
    df['series_binary'] = df['series'].apply(lambda x: 1 if '#' in x else 0)
    df.drop('series', axis=1, inplace=True)

    df['places'].replace(np.nan, 'missing', inplace=True)
    df['places'].replace(['All Editions | Add a New Edition | Combine', ''], 'missing', inplace=True)

    df['url'].replace(np.nan, 'missing', inplace=True) # 1532 values missing drop it

    df['publish_year'] = df['publish_year'].astype(str)
    keep_year = df['publish_year'].apply(lambda x: x.split('by')[0])
    df['publish_year'] = keep_year.apply(lambda x: x.replace('Published ', ''))
    df['publish_year'] = df['publish_year'].apply(lambda x: x.replace('st', ',').replace('th', ',').replace('rd', ','))

    return df


def preprocessing(df):
    scaler = MinMaxScaler((1, 10))
    df['minmax_norm_rating'] = scaler.fit_transform(df[['rating']])
    df['mean_norm_ratings'] = 1 + (df['rating'] - df['rating'].mean()) / (df['rating'].max() - df['rating'].min()) * 9
    return df

def analyse(df):
    pass

def main():
    df = scrape('books_2000.csv')
    clean_df = data_clean(df)
    processed_df = preprocessing(clean_df)
    analyse(processed_df)


if __name__ == '__main__':
    main()

