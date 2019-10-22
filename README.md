<p align="center"><img src="images/hearhere_logo.png"></p>

## About
> Measure local reputation of global banking

HearHere analyzes the opinion generated by banks around their branches to understand their acceptance in each community.

### Requeriments

Install the needed libraries for the project:

```
pip3 install requests
pip3 install pandas
pip3 install bs4
```

### Data sources

Locations extracted from:

- [BBVA - Branch and Cashier Locator](https://www.bbva.es/general/localizador-oficinas-cajeros/index.jsp) - Main data source

### Project structure

##### Files:

- **main.ipynb**: Jupyter file with HH queries setup and visualization
- **scrapers.py**: Download data from web
- **config.py**: Project paths configuration

##### Folders:

- **data**: Data from scraping
- **images**