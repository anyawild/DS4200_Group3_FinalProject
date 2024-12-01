""""
File: dashapi.py

Description: The primary API for interacting with the 'ds4200_project_co2_data.csv' dataset.
"""

import pandas as pd
import numpy as np



class DASHAPI:

    data = None
    countries = None

    def load_data(self, filename):
        self.data = pd.read_csv(filename)
        print(self.data)

    def clean_data(self):
        """ filters out rows of data by checking if it contains a substring from each elements of the filter list"""
        # trying to manually filter out each non-country entry,
        not_countries = ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Antarctica', '(GCP)', 'Bermuda',
                         'International', 'Zone', 'countries', 'Fires', 'OECD', 'Wallis', 'Anguilla',
                         'Bonaire',
                         'British Virgin Islands', 'Christmas Island', 'Cook Islands', 'Curacao', 'Faroe Islands',
                         'French Polynesia', 'Greenland', 'Hong Kong', 'Leeward Islands', 'Macao', 'Montserrat',
                         'New Caledonia', 'Oceania', 'Palestine', 'Ryukyu Islands', 'Saint Helena', 'Saint Pierre',
                         'Turks and Caicos Islands']
        self.countries = np.unique(self.data[['country']])
        self.countries = [country for country in self.countries if not any(str in country for str in not_countries)]
        self.countries = sorted(self.countries)
        self.data = self.data.loc[(self.data['country'].isin(self.countries))]
        self.data = self.data.loc[(self.data['year'] >= 1851)]

    def get_countries(self):
        """ Fetch the list of all unique countries listed in this dataset """

        # if there is any trace of any of the elements in 'not_countries', filters out from countries lst
        # this method did end up filtering out South Africa and Central African Republic

        return self.countries

    def extract_countries(self, country=None, gdp_range=None, year=None):
        """ Extracts slice of dataset for use in visualization, with the country selected
        """

        copy = self.data.copy()
        #gdp multiplied by billion
        gdp_low, gdp_high = gdp_range
        gdp_low *= 1000000000
        gdp_high *= 1000000000
        # Essentially making the World option display every country instead of just the 'World' entry
        if country == 'World':
            #filtering by year and exlcuding the outlier
            copy = copy.loc[(copy['year'] >= year[0]) & (copy['year'] <= year[1])]
            #filtering by country gdp
            copy = copy.loc[(copy['gdp'] >= gdp_low) & (copy['gdp'] <= gdp_high)]
        else:
            # otherwise just filter for the specific country
            # keeping world in order to make calculations
            copy = copy.loc[(copy['country'] == country) & (copy['year'] >= year[0]) & (copy['year'] <= year[1])]

        world = self.data.loc[(self.data['country'] == 'World') & (self.data['year'] >= year[0]) & (self.data['year'] <= year[1])]
        copy = pd.concat([copy, world])

        return copy

    def extract_filter_countries(self, country_lst = ['United States'], year = None):
        copy = self.data.copy()
        copy = copy[copy['country'].isin(country_lst)]
        copy = copy.loc[(copy['year'] >= year[0]) & (copy['year'] <= year[1])]
        return copy

def main():
    print("hello world")

if __name__ == '__main__':
    main()