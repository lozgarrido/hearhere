<img src="images/hearhere_readme_logo.png" alt="logo" title="HearHere logo" style="margin: 20px" align="middle"/>

> Measure local reputation of global banking

**HearHere** analyzes the opinion generated by banks around their branches to improve their acceptance in each community.

## About

### Requeriments

Install the needed libraries for the project. They are also included in *requirements.txt* file.

```
pip3 install requests
pip3 install pandas
pip3 install numpy
pip3 install bs4
pip3 install googlemaps
pip3 install twint
```

### First steps

Open the *main.ipynb* file with [Jupyter Notebook](https://jupyter.org) and follow the instructions.

A valid [Google Cloud Platform](https://cloud.google.com/maps-platform/) API key is needed to update the database. If you have one, you can edit the *api_keys.py* file with it.


## Files structure

### Code

- **main.ipynb**: Jupyter file with HH queries setup and visualization
- **locations_scraper.py**: Downloads data from web
- **twitter_scraper.py**: Downloads tweets
- **files_updater.py**: Call the scrapers to update the databases
- **google_maps_api.py**: Conects HH with Google Cloud
- **config.py**: Project paths configuration
- api_keys.py*

### Folders

- **data**: Data from scraping
- **images**


## Attributions

### Data sources

- [BBVA - Branch and Cashier Locator](https://www.bbva.es/general/localizador-oficinas-cajeros/index.jsp) - BBVA branches locations
- [Twitter](https://twitter.com/) - Related tweets

Connected APIs:

- [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/start) - Full addresses and coordinates

### Road map (next steps)

- Incorporate Google Maps reviews from Place_ID **(in progress)**
- Improve the amount and quality of information retrieved with APIs **(in progress)**
- Add new banks so that they can be compared with each other
- Improve code efficiency
- Expand the tool to other sectors
- Port the tool out of the development environment

### Acknowledgements

HearHere was the final project of Ironhack's Data Analysis bootcamp. Thank you to everyone who made it possible.