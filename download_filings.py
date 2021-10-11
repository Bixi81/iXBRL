from bs4 import BeautifulSoup 
from urllib.request import urlopen 
import requests, time, traceback, random, csv, codecs, re, os
from datetime import datetime
import urllib.request

res = requests.get("https://filings.xbrl.org/")
soup = BeautifulSoup(res.text, 'html.parser')
tr = soup.find_all('tr')
for c,t in enumerate(tr):
    country = t.find('td',{'class':'country'})
    if "DE" in str(country):
        
        date = t.find('td',{'class':'date'})
        date = date.text#[:4]
        date = date.replace("-","")
        
        ent = t.find('td',{'class':'entity'})
        ent = ent.text.replace("[ LEI ]","")
        ent = ''.join(ent.split())
        ent = ent.replace(" ","").replace(".","").replace("&","")
        
        for x in t.find_all('td',{'class':'icon-column'}):
            if ".zip" in str(x).lower():
                x = str(x)
                x = x[x.find("href=")+6:]
                x = x[:x.find(">")-1]                
                #filename = x[x.rfind("/")+1:]
                filename = date + "_" + ent + ".zip"
                # https://filings.xbrl.org/2594002H3ZAFID0MP378/2020-12-31/ESEF/PL/0/2594002H3ZAFID0MP378-2020-12-31.zip
                try:
                    #print("https://filings.xbrl.org/"+str(x))
                    print("Download",filename)
                    urllib.request.urlretrieve("https://filings.xbrl.org/"+str(x), "D:/"+str(filename))
                    time.sleep(0.5)
                except:
                    print("Error in",filename)
                    continue
