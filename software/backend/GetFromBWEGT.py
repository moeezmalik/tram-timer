import requests
from bs4 import BeautifulSoup as bs
from enum import Enum
import yaml
import pytz
from datetime import datetime



class Status(Enum):
    ALL_GOOD = 1            # This will be generated when everything goes well
    HTTP_ERROR = 2          # This will be generated when the BWEGT server throws an error
    MOT_NOT_FOUND = 3       # This will be generated when Mode of Transport is not found

def getDifferenceInMinutes(vehicle_time):
    ###############################################
    # Get the ETA
    ###############################################

    # Getting the current time for Germany

    de_tz = pytz.timezone('Europe/Berlin')
    now_time = datetime.now(de_tz)
    now_time = now_time.replace(second = 0, microsecond = 0, tzinfo = None)

    now_year = now_time.year
    now_month = now_time.month
    now_day = now_time.day

    now_hour = now_time.hour
    now_minute = now_time.hour
    now_second = now_time.second

    # Adapting the time of tram

    vehicle_hour_and_minute = vehicle_time.split(':')

    vehicle_year = now_year
    vehicle_month = now_month
    vehicle_day = now_day

    vehicle_hour = int(vehicle_hour_and_minute[0])
    vehicle_minute = int(vehicle_hour_and_minute[1])
    vehicle_second = 0

    if(vehicle_hour < now_hour):
        vehicle_day += 1

    vehicle_time = datetime(vehicle_year, vehicle_month, vehicle_day, vehicle_hour, vehicle_minute, vehicle_second)

    td = vehicle_time - now_time
    ETA_minutes = td.seconds // 60 % 60

    return ETA_minutes

def getETA(vehicle_times):
    eta = getDifferenceInMinutes(vehicle_times[0])

    if(eta == 0):
        eta = getDifferenceInMinutes(vehicle_times[1])

    return eta

def getHTMLContent(stop_id):
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

    url = url.format(stop_id, stop_id)
    url = url.replace("\n","")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    return response.status_code, response.content

def getNextTwoVehicleTimes(html_content, stop_id, target_line, target_direction):
    soup = bs(html_content, 'html.parser')

    # Get the Element that contains the city and the station name
    city_and_stop = soup.find('span', {'class' : 'std3_odv-min-group'}).text

    # Extract just the station name from it
    stop_name = city_and_stop.split(", ")[1]

    # Find all mode of transportations
    results = soup.find_all('div', {'class' : '''std3_col-xs-12 std3_full-size std3_departure-line std3_result-row std3_assigned-StopID-{} {}'''.format(stop_id, stop_id)})

    # Iterate until the earliest specified mode of transport is found

    count = 0
    vehicle_times = ['null', 'null']

    for result in results:
        heute_zeit = result.find('div', {'class' : 'std3_dm-time std3_dm-result-row'})
        echt_zeit = result.find('div', {'class' : 'std3_dm-time std3_dm-result-row std3_realtime-column'})
        richtung = result.find('a', {'class' : 'std3_trip-stop-times-trigger'})
        mot_und_linie = result.find('span', {'class' : 'std3_mot-label'}).text
        mot_und_linie = mot_und_linie.split()
        mot = mot_und_linie[0]
        linie = mot_und_linie[1]

        if (linie == target_line and richtung.text == target_direction):

            print(f"Geplannt Zeit: {heute_zeit.text}")
            print(f"Echt Zeit: {echt_zeit.text}")
            print(f"Linie: {linie}")
            print(f"Richtung: {richtung.text}")
            print()

            vehicle_times[count] = echt_zeit.text
            count += 1

            if(count == 2):
                break

    return vehicle_times

def getETAOfNextMOT(stop_id, target_line, target_direction):

    reply = {'status' : Status.ALL_GOOD, 'response' : {}}

    status_code, content = getHTMLContent(stop_id)

    if(status_code == 200):

        vehicle_times = getNextTwoVehicleTimes(content, stop_id, target_line, target_direction)

        if(vehicle_times[0] != 'null' and vehicle_times[0] != 'null'):
            eta = getETA(vehicle_times)
            reply['response'] = eta
        else:
            reply['status'] = Status.MOT_NOT_FOUND

    else:
        reply['status'] = Status.HTTP_ERROR


    if(reply['status'] == Status.ALL_GOOD):
        print("Vehicle comes in {} min".format(eta))
    else:
        print("Some Error Occurred")

    print()

