import pandas as pd
import numpy as np
from google_maps_api import extract_geocode
from twitter_scraper import retrieve_tweets


def bbva_update_offices(bbva_offices_path):
    """
    Scrap BBVA offices from the web, clean the data and exports it in the given .csv path

    :param bbva_offices_path: .csv file that will be updated
    :return: DataFrame with data
    """

    from locations_scraper import bbva_extract_offices

    #Scrap the offices
    bbva_offices = bbva_extract_offices()

    #Drop unneeded columns
    bbva_offices = bbva_offices.drop(columns=['office_url',
                                              'municipality_name',
                                              'municipality_url',
                                              'province_name',
                                              'province_url'])

    #Drop empty rows
    bbva_offices.replace('', np.nan, inplace=True)
    bbva_offices = bbva_offices.dropna()

    #Retrieve location info from Google Maps API
    address_column = 'office_direction'
    bbva_offices['geo_extraction'] = bbva_offices.apply(lambda row: extract_geocode(row[address_column]), axis=1)

    #Drop offices without any match
    bbva_offices.replace('', np.nan, inplace=True)
    bbva_offices = bbva_offices.dropna()

    #Convert the new info into columns and remove the old ones
    geo_extraction_items = ['address', 'latitude', 'longitude', 'place_id']
    bbva_offices[geo_extraction_items] = pd.DataFrame(bbva_offices.geo_extraction.values.tolist(),
                                                      index=bbva_offices.index)
    bbva_offices = bbva_offices.drop(columns=['office_direction',
                                              'geo_extraction'])

    #Drop duplicates
    bbva_offices.drop_duplicates(subset='place_id', inplace=True)

    #Export dataset and return it as DataFrame
    bbva_offices.to_csv(bbva_offices_path, index=False)
    return bbva_offices


def bbva_update_tweets(bbva_offices_path, bbva_tweets_path):
    """
    Search tweets related to BBVA near from its branches and build a dataset from them

    :param bbva_offices_path: .csv file that will be updated with locations
    :param bbva_tweets_path: .csv file that will be updated with tweets corpus
    :return: DataFrame with tweets
    """

    bbva_offices = pd.read_csv(bbva_offices_path)

    #Create an empty DataFrame
    bbva_tweets = pd.DataFrame()

    #Iterate over all BBVA branches locations
    for index, values in bbva_offices.iterrows():
        latitude = values['latitude']
        longitude = values['longitude']

        # Retrieve tweets for given coordinates
        located_tweets = retrieve_tweets('bbva', latitude, longitude)

        try: #If there are tweets
            if located_tweets['tweet']:

                #Add office-related data for visualization
                located_tweets['office_number'] = str(values['office_number'])
                located_tweets['address'] = str(values['address'])
                located_tweets['latitude'] = str(latitude)
                located_tweets['longitude'] = str(longitude)


                #Append tweets to 'bbva_tweets' dataset
                bbva_tweets = bbva_tweets.append(located_tweets, ignore_index=True)
                print(located_tweets)

        except: #If there aren't results
            pass

    # Export the entire DataFrame as .csv
    bbva_tweets.to_csv(bbva_tweets_path, index=False)
    return bbva_tweets
