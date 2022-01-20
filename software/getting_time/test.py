from datetime import datetime 
import requests
from bs4 import BeautifulSoup as bs
import re

dt=datetime.today()

url='''
https://efa.vagfr.de/vagfr3/XSLT_DM_REQUEST?
language=de&
std3_suggestMacro=std3_suggest&
std3_commonMacro=dm&
itdLPxx_contractor=&
std3_contractorMacro=&
includeCompleteStopSeq=1&
mergeDep=1&
mode=direct&
useRealtime=1&
name_dm=Freiburg+im+Breisgau%2C+Paula-Modersohn-Platz&
nameInfo_dm=6930651&
type_dm=any&
itdDateDayMonthYear={}.{}.{}&
itdTime={}%3A{}&
itdDateTimeDepArr=dep&
includedMeans=checkbox&
itdLPxx_ptActive=on&
useRealtime=1&
inclMOT_0=true&inclMOT_1=true&inclMOT_2=true&inclMOT_4=true&inclMOT_5=true&inclMOT_6=true&inclMOT_7=true&inclMOT_10=true&inclMOT_11=true&
sessionID=0&
requestID=0&
itdLPxx_directRequest=1&
coordOutputFormat=WGS84[dd.ddddd]&
itdLPxx_timeFormat=24
'''.format(dt.day,dt.month,dt.year,dt.hour,dt.minute)

url=url.replace("\n","")

page=requests.get(url)
soup=bs(page.content,"html.parser")

result = soup.find_all("div", {"class": "std3_dm-result_container"})

print("Result: ")
print(result)

data=[]
for i in range(0,len(result)):
    dm_mot_info=result[i].find("div",{"class":"std3_dm-mot-info"}).text
    val=dm_mot_info.strip(' ').split()[1]
    line,direct=re.findall('\d+|\D+', val)
    
    dm_time=result[i].find("div",{"class":"std3_dm-time std3_dm-result-row"}).text
    dm_realtime=result[i].find("div",{"class":"std3_dm-time std3_dm-result-row std3_realtime-column"}).text
    
    data.append((line,direct,dm_time,dm_realtime))

print("Data: ")
print(data)
