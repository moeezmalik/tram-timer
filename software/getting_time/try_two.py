import requests
from bs4 import BeautifulSoup as bs
import re
import urllib3

url = '''
https://preview.efa-bw.de/efabw_preview/XSLT_DM_REQUEST?
language=de&
std3_suggestMacro=std3_suggest&
std3_commonMacro=dm&
itdLPxx_contractor=eva&
std3_contractorMacro=eva&
includeCompleteStopSeq=1&
mergeDep=1&
useRealtime=1&
mode=direct&
name_dm=Freiburg+im+Breisgau%2C+Paula-Modersohn-Platz&
type_dm=any&
nameInfo_dm=6930651&
deleteAssignedStops=1&
line=all&
includedMeans=checkbox&
useRealtime=1&
std3_inclMOT_0Macro=true&
std3_inclMOT_1Macro=true&
std3_inclMOT_2Macro=true&
std3_inclMOT_3Macro=true&
std3_inclMOT_4Macro=true&
std3_inclMOT_5Macro=true&
std3_inclMOT_6Macro=true&
std3_inclMOT_8Macro=true&
std3_inclMOT_9Macro=true&
std3_inclMOT_10Macro=true&
std3_inclMOT_11Macro=true&
inclMOT_7=1&
inclMOT_12=1&
inclMOT_13=1&
inclMOT_14=1&
inclMOT_15=1&
inclMOT_16=1&
inclMOT_17=1&
inclMOT_18=1&
inclMOT_19=1&
imparedOptionsActive=1&
sessionID=0&
requestID=0&
itdLPxx_directRequest=1&
coordOutputFormat=WGS84[dd.ddddd]'''

url = url.replace("\n","")
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

# Beautiful Soup Starts Here

soup = bs(response.content, 'html.parser')
results = soup.find_all('div', {'class' : 'std3_col-xs-12 std3_full-size std3_departure-line std3_result-row std3_assigned-StopID-6930651 6930651'})

for result in results:
    heute_zeit = result.find('div', {'class' : 'std3_dm-time std3_dm-result-row'})
    echt_zeit = result.find('div', {'class' : 'std3_dm-time std3_dm-result-row std3_realtime-column'})

    print(f"Geplannt Zeit: {heute_zeit.text}")
    print(f"Echt Zeit: {echt_zeit.text}")
    print()

with open("output2.html", "w") as file:
    file.write(str(results))
