import requests
from bs4 import BeautifulSoup as bs
from enum import Enum
import yaml

class Status(Enum):
    ALL_GOOD = 1            # This will be generated when everything goes well
    HTTP_ERROR = 2          # This will be generated when the BWEGT server throws an error
    MOT_NOT_FOUND = 3       # This will be generated when Mode of Transport is not found


haltestelle_nummer = 6930651
target_linie = '3'
target_richtung = 'Haid'

###############################################
# Load Configurations 
###############################################

# Load the YAML file for getting configurations
with open('config.yml') as f:
    config = yaml.load(f, Loader = yaml.FullLoader)

# Get the URL from the YAML file
url = config['url']

###############################################
# Load URL 
###############################################

url = url.format(haltestelle_nummer, haltestelle_nummer)
url = url.replace("\n","")
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

###############################################
# Process the URL and get information
###############################################



soup = bs(response.content, 'html.parser')

# Get the Element that contains the city and the station name
stadt_und_haltestelle = soup.find('span', {'class' : 'std3_odv-min-group'}).text

# Extract just the station name from it
haltestelle_name = stadt_und_haltestelle.split(", ")[1]

# Find all mode of transportations
results = soup.find_all('div', {'class' : '''std3_col-xs-12 std3_full-size std3_departure-line std3_result-row std3_assigned-StopID-{} {}'''.format(haltestelle_nummer, haltestelle_nummer)})

# Iterate until the earliest specified mode of transport is found
for result in results:
    heute_zeit = result.find('div', {'class' : 'std3_dm-time std3_dm-result-row'})
    echt_zeit = result.find('div', {'class' : 'std3_dm-time std3_dm-result-row std3_realtime-column'})
    richtung = result.find('a', {'class' : 'std3_trip-stop-times-trigger'})
    mot_und_linie = result.find('span', {'class' : 'std3_mot-label'}).text
    mot_und_linie = mot_und_linie.split()
    mot = mot_und_linie[0]
    linie = mot_und_linie[1]

    if (linie == target_linie and richtung.text == target_richtung):

        print(f"Geplannt Zeit: {heute_zeit.text}")
        print(f"Echt Zeit: {echt_zeit.text}")
        print(f"Linie: {linie}")
        print(f"Richtung: {richtung.text}")
        print()

        break

print(url)
# FOR DEBUGGING PURPOSES
# with open("output2.html", "w") as file:
#     file.write(str(results))
