import requests
import pandas as pd
from bs4 import BeautifulSoup


def bbva_extract_locations(url):
    """
    Scrap locations from any depth of bbva.es offices directory

    :param url: url to be scrapped
    :return: list of locations info as dictionaries
    """

    bbva_url = 'https://www.bbva.es'
    locations = []

    # Soup config
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrap location when it has a proper format
    for row in soup.find_all('a', href=True):
        if '/general/oficinas/' in row['href'] and row.get('id') != 'volverProvincia':
            location_url = bbva_url + row['href']
            location_name = row.get('title')

            # If 'title' attribute doesn't exist, extract it from url
            if not location_name:
                location_name = location_url.split('/')[-1].capitalize()

            # Define office output
            if 'Ver oficina' in row.get_text():
                office_direction = row.get_text().replace('Ver oficina', '')
                location_info = {
                    'office_number': location_name,
                    'office_url': location_url,
                    'office_direction': office_direction
                }

                # Define province output
            elif row.find('span'):
                location_info = {
                    'province_name': location_name,
                    'province_url': location_url,
                }

                # Define municipality output
            else:
                location_info = {
                    'municipality_name': location_name,
                    'municipality_url': location_url,
                }

            locations.append(location_info)  # Append output to 'locations' list

    return locations


def bbva_extract_offices(dataframe=True):
    """
    Call 'bbva_extract_locations()' recursively on all bbva.es offices directory

    :dataframe: config the output
    :return: DataFrame or list of dicts
    """

    bbva_locations_directory = 'https://www.bbva.es/general/localizador-oficinas-cajeros/index.jsp'

    # Return provincies with bank presence
    bbva_provinces = bbva_extract_locations(bbva_locations_directory)

    # Return municipalities from provincies
    bbva_municipalities = []
    for province in bbva_provinces:
        province_municipalities = bbva_extract_locations(province['province_url'])

        # Append province info to municipality in 'bbva_municipalities' list
        for municipality in province_municipalities:
            municipality['province_name'] = province['province_name']
            municipality['province_url'] = province['province_url']
            bbva_municipalities.append(municipality)

    # Return offices from municipalities
    bbva_offices = []
    for municipality in bbva_municipalities:
        municipality_offices = bbva_extract_locations(municipality['municipality_url'])

        # Append municipality and province info to office in 'bbva_offices' list
        for office in municipality_offices:
            office['municipality_name'] = municipality['municipality_name']
            office['municipality_url'] = municipality['municipality_url']
            office['province_name'] = municipality['province_name']
            office['province_url'] = municipality['province_url']
            bbva_offices.append(office)

    #Convert output to DataFrame
    if dataframe == True:
        bbva_offices = pd.DataFrame(bbva_offices)

    return bbva_offices