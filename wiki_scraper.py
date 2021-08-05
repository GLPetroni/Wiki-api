import argparse
import requests
import urllib.request
import time
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen

def process_num(num):
    return float(re.sub(r'[^\w\s.]','',num))

#####################################
# Split address into readable format
#####################################
def split(address):
    tmp = re.findall('[A-Z][^A-Z]*', address)
    tmp = ' '.join(tmp)
    return tmp

#####################################
# Format cords into decinals and remove N,W,S,E
#####################################
def format_cords(cord):
    parts = re.split('[ ]', cord)
    parts1 = re.split('[°]',parts[0])
    parts2 = re.split('[°]',parts[1])
    if parts1[1] == "S":
       parts1[0] = -1 * float(parts1[0])
    if parts2[1] == "W":
       parts2[0] = -1 * float(parts2[0])
    parts[0] = str(parts1[0])
    parts[1] = str(parts2[0])
    cord = " ".join(parts)
    return cord

#####################################
# main function: takes url and scrapes wiki page for address, coordinates, and year opened
#####################################
def main(url):
    html = urlopen(url) 
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find('table', {"class":"infobox vcard ib-station"})

    Image = []
    Address = []
    Coordinates = []
    Open_year = []
    
    for table in tables:
        rows = table.find_all('tr')

        for opened in rows:


            opened = soup.find("th", string="Opened")
            Open_year.append(opened.find_next("td", {"class": "infobox-data"}).text)

            location = soup.find("th", string="Location")
            Address.append(location.find_next("td").text)

            cord= soup.find("span", {"class": "geo-dec", "title":"Maps, aerial photos, and other data for this location"})
            Coordinates.append(cord.text)
    
    cord = format_cords(Coordinates[0])
    address = split(Address[0])
    print("Address: ",address)
    print("Coordinates: ",cord)
    print("Year Opened: ",Open_year[0])
    year = str(Open_year[0])
    _dict = {"address":address, "cord":cord, "year":year}
    return _dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help = "Show Output")
    args = parser.parse_args()
    main(args.u)
