import re
import googlemaps


def launch_google_maps_api():
    """
    Initialize the Google Maps API

    :return: API generator
    """

    # Import Google Maps API key and setup the library
    from config import geocoding_api_key
    if geocoding_api_key == '':
        from api_keys import geocoding_api_key

    #Activate the API and return its generator
    gmaps = googlemaps.Client(key=geocoding_api_key)
    return gmaps


def extract_geocode(address):
    """
    Recover full address, coordinates and place ID from Google Maps API

    :param address: address
    :return: list of items (address, lat., lng. and place ID)
    """

    #Create the API generator
    gmaps = launch_google_maps_api()

    # Build the parameters
    address = 'BBVA ' + address
    address = re.sub(r'[^0-9a-zA-Z]+', '+', address)

    parameters = {
        'address': address,
        'region': 'es'
        }

    # Call the API and access to the first result if there are more
    geocode_result = gmaps.geocode(parameters)

    try:
        geocode_result = geocode_result[0]

        # Define variables
        formatted_address = geocode_result['formatted_address']
        lat = geocode_result['geometry']['location']['lat']
        lng = geocode_result['geometry']['location']['lng']
        place_id = geocode_result['place_id']

        # Return requested data as a list
        new_info = [formatted_address, lat, lng, place_id]
        return new_info

    # No results
    except:
        return ('')
