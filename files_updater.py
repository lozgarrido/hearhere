from google_maps_api import extract_geocode
import pandas as pd
import numpy as np


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
