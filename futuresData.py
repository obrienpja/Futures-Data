# Author: Patrick James O'Brien
# Note: I acknowledge that this code is not PEP 8 compliant. I need to learn more
# and make some changes in order to make it PEP 8 compliant.

from urllib import *
from bs4 import BeautifulSoup
import sys
from datetime import date
import os
import collections

# Headers required to request html page
hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

# All commodities links we are interested in
all_links = ['http://www.cmegroup.com/trading/agricultural/grain-and-oilseed/corn_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean-oil_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/agricultural/grain-and-oilseed/soybean-meal_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/agricultural/grain-and-oilseed/wheat_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/agricultural/livestock/live-cattle_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/agricultural/livestock/lean-hogs_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/energy/crude-oil/light-sweet-crude_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/energy/natural-gas/natural-gas_quotes_settlements_futures.html', 'http://www.cmegroup.com/trading/energy/crude-oil/brent-crude-oil-last-day_quotes_settlements_futures.html', 'http://cmegroup.com/trading/energy/refined-products/rbob-gasoline_quotes_settlements_futures.html?0.39051251617231486=', 'http://cmegroup.com/trading/energy/refined-products/heating-oil_quotes_settlements_futures.html', 'http://cmegroup.com/trading/energy/crude-oil/emini-crude-oil_quotes_settlements_futures.html', 'http://cmegroup.com/trading/energy/natural-gas/emini-natural-gas_quotes_settlements_futures.html', 'http://cmegroup.com/trading/interest-rates/stir/eurodollar_quotes_settlements_futures.html', 'http://cmegroup.com/trading/interest-rates/us-treasury/2-year-us-treasury-note_quotes_settlements_futures.html', 'http://cmegroup.com/trading/interest-rates/us-treasury/5-year-us-treasury-note_quotes_settlements_futures.html', 'http://cmegroup.com/trading/interest-rates/us-treasury/10-year-us-treasury-note_quotes_settlements_futures.html', 'http://cmegroup.com/trading/interest-rates/us-treasury/ultra-10-year-us-treasury-note_quotes_settlements_futures.html', 'http://cmegroup.com/trading/interest-rates/us-treasury/30-year-us-treasury-bond_quotes_settlements_futures.html', 'http://cmegroup.com/trading/interest-rates/us-treasury/ultra-t-bond_quotes_settlements_futures.html', 'http://cmegroup.com/trading/equity-index/us-index/e-mini-sandp500_quotes_settlements_futures.html', 'http://cmegroup.com/trading/equity-index/us-index/e-mini-nasdaq-100_quotes_settlements_futures.html', 'http://cmegroup.com/trading/equity-index/us-index/e-mini-dow_quotes_settlements_futures.html', 'http://cmegroup.com/trading/equity-index/international-index/nikkei-225-yen_quotes_settlements_futures.html', 'http://cmegroup.com/trading/equity-index/select-sector-index/e-mini-financial-select-sector_quotes_settlements_futures.html', 'http://cmegroup.com/trading/equity-index/us-index/e-mini-russell-2000_quotes_settlements_futures.html' ,'http://cmegroup.com/trading/equity-index/us-index/e-mini-sandp-midcap-400_quotes_settlements_futures.html', 'http://cmegroup.com/trading/fx/g10/australian-dollar_quotes_settlements_futures.html', 'http://cmegroup.com/trading/fx/g10/canadian-dollar_quotes_settlements_futures.html', 'http://cmegroup.com/trading/fx/g10/swiss-franc_quotes_settlements_futures.html', 'http://cmegroup.com/trading/fx/g10/euro-fx_quotes_settlements_futures.html', 'http://cmegroup.com/trading/fx/g10/british-pound_quotes_settlements_futures.html', 'http://cmegroup.com/trading/fx/g10/japanese-yen_quotes_settlements_futures.html', 'http://cmegroup.com/trading/fx/emerging-market/mexican-peso_quotes_settlements_futures.html', 'http://cmegroup.com/trading/metals/precious/gold_quotes_settlements_futures.html', 'http://cmegroup.com/trading/metals/precious/silver_quotes_settlements_futures.html', 'http://cmegroup.com/trading/metals/precious/platinum_quotes_settlements_futures.html', 'http://cmegroup.com/trading/metals/precious/palladium_quotes_settlements_futures.html', 'http://cmegroup.com/trading/metals/base/copper_quotes_settlements_futures.html', 'http://cmegroup.com/trading/metals/precious/e-micro-gold_quotes_settlements_futures.html', 'http://cmegroup.com/trading/metals/precious/1000-oz-silver_quotes_settlements_futures.html']

names = ['corn', 'soybean', 'soybean-oil', 'soybean-meal', 'wheat', 'live-cattle', 'live-hogs', 'light-sweet-crude', 'natural-gas', 'brent-crude-oil-last-day', 'rbob-gasoline', 'heating-oil', 'emini-crude-oil', 'emini-natural-gas', 'eurodollar', '2-year-us-treasury-note', '5-year-us-treasury-note', '10-year-us-treasury-note', 'ultra-10-year-us-treasury-note', '30-year-us-treasury-bond', 'ultra-t-bond', 'e-mini-sandp500', 'e-mini-nasdaq-100', 'e-mini-dow', 'nikkei-225-yen', 'e-mini-financial-select-sector', 'e-mini-russell-2000', 'e-mini-sandp-midcap-400', 'australian-dollar', 'canadian-dollar', 'swiss-franc', 'euro-fx', 'british-pound', 'japanese-yen', 'mexican-peso', 'gold', 'silver', 'platinum', 'palladium', 'copper', 'e-micro-gold', '1000-oz-silver']


# Create directory path for a given date in which we will dump data
def create_directory_name(date_val):
	return '/home/solidangle/Jobs/Resume/Practice Codes/Charles/' + date_val.strftime('%m_%d_%Y')


# Create directory in which we will dump data
def create_date_directory(date_val):
	os.mkdir(create_directory_name(date_val))


# Construct full link for a commodity base link and a date
def assemble_link(single_link, date_val):
    return single_link + '#tradeDate=' + date_val


# Dump data for a given commodity link and date to a given filepath
def dump_data(commodity, file_name, date_val):
    # Construct link from which we pull data
    quote_page = assemble_link(commodity, date_val)

    # Request to open html page
    req = request(quote_page, headers=hdr)

    # Open html page
    page = urlopen(req)

    # Parse html so that we can filter out data
    soup = BeautifulSoup(page, 'html.parser')

    # Remove table from the html
    table_info = soup.tbody.find_all('tr')

    # Open a file to write data
    f = open(directory + '/' + file_name, 'w')

    # Write data columns to a file
    for i in table_info:
        f.write(i.find('th').text.strip() + ' ')
        row = i.find_all('td')
        for j in row:
            f.write(j.text.strip() + ' ')
        f.write('\n')


# Dump data for all commodities links
def dump_all_data(date_val):
    for i in range(len(all_links)):
        dump_data(all_links[i], names[i], date_val)


# Run the data process, which will only get data if a data directory does not already exist
def data_retrieval(date_val):
	if not os.path.isdir(create_directory_name(date_val)):
    	create_date_directory(date_val)
   		dump_all_data(date_val)


data_retrieval('07/17/2017')
# data_retrieval(date.today())
