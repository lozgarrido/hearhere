import twint
from datetime import date, timedelta
import nest_asyncio
nest_asyncio.apply()  # Avoid ocassional RuntimeError in Jupyter Notebook


def retrieve_tweets(keyword, latitude, longitude, radius='1.00km'):
    """
    Returns tweets mentioning the keyword made in the last year around the given coordinates

    :param keyword: string to search
    :param latitude: as string, with dot for decimals
    :param longitude: as string, with dot for decimals
    :param radius: as string, with dot for decimals
    :return: DataFrame with found tweets
    """

    # Build parameters
    today = str(date.today())
    a_year_ago = str(date.today() - timedelta(365))
    location_parameters = (latitude + ', ' + longitude + ', ' + radius)

    # Config the query
    c = twint.Config()
    c.Search = keyword
    c.Pandas = True

    # Config dates range
    c.Since = a_year_ago
    c.Until = today

    # Config location
    c.Location = True
    c.Geo = location_parameters

    # Make the request
    twint.run.Search(c)
    located_tweets = twint.storage.panda.Tweets_df
    return located_tweets