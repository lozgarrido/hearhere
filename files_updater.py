from google_maps_api import extract_geocode
import pandas as pd
import numpy as np


def update_bbva_offices(bbva_offices_path):
    """
    Scrap BBVA offices from the web, clean the data and exports it in the given .csv path

    :param bbva_offices_path: .csv file that will be updated
    :return: DataFrame with data
    """

    from scrapers import bbva_extract_offices

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

    #Drop offices without a match
    bbva_offices = bbva_offices.dropna()

    #Format DataFrame with the new info
    #requested_data = ['address', 'latitude', 'longitude', 'place_id']
    #bbva_offices[requested_data] = pd.DataFrame(bbva_offices.geo_extraction.values.tolist())
    #bbva_offices = bbva_offices.drop(columns=['geo_extraction'])

    #Remove rows without information
    bbva_offices = bbva_offices.dropna(how='any')

    #Export dataset and return it as DataFrame
    bbva_offices.to_csv(bbva_offices_path, index=False)
    return bbva_offices
