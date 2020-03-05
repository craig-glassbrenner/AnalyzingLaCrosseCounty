"""
    Craig Glassbrenner, CS461

    This is a webScraper program, it scrapes the La Crosse County Land Records Portal
    for parcel information including Municipality, Total Acreage, and Street Address
    along with Tax information such as: Land Value, Improved Value, and Total value.

    Reads the data from the website and stores html data in html files while storing 
    json data in json files for both 2018 and 2019.
"""

#Imports
import requests
import time
import os
import random
from bs4 import BeautifulSoup

# Scrapping HTML received from the website storing them in html files in my webscraping directory. 
def htmlScraper():
    random.seed(24)
    i=0
    print('HTML: \n')
    # Reading 1000 different homes data
    while(i < 1000):
        parcelId = random.randint(1, 73033)
        print(parcelId)
        
        filepath = os.path.join('/Users/craigglassbrenner/Desktop/WebScraping/data/html', 'p' + str(parcelId) + '-2019.html')
        f = open(filepath, 'w+')
        
        params = {'ParcelID' : parcelId, 'TaxYear': '2019'}
        response = requests.get("https://apps.lacrossecounty.org/LandRecordsPortal/PrintParcel.aspx", params = params)

        soup = BeautifulSoup(response.content, "html.parser")
        s = soup.find_all('td')
        counter = 0;

        # Variables of interest
        munc = ''
        acreage = 0
        city = ''
        address = ''
        worked = True

        # Getting values for the data we care about
        for l in s:
            try:
                l = l.string.replace('<td>','').replace('</td', '').replace(':', '')
            except:
                worked = False
                pass
            
            if(l == 'Municipality'):
                l = s[counter+1].string.replace('<td>','').replace('</td', '').replace(':', '')
                munc = munc + l
            elif(l == 'Total Acreage'):
                l = s[counter+1].string.replace('<td>','').replace('</td', '').replace(':', '')
                acreage = float(l)

            elif(l == 'City(Postal)'):

                try:
                    l = s[counter+1].string.replace('<td>','').replace('</td', '').replace(':', '')
                    address = s[counter+1].string.replace('<td>','').replace('</td', '').replace(':', '')
                    print(address + '\n')
                    city = s[counter+2].string.replace('<td>','').replace('</td', '').replace(':', '')

                except:
                    address = 'None'
                    city = 'None'

            if(munc != '' and acreage != 0 and city != '' and address != ''):
                break
            counter = counter + 1

        # Writing to file otherwise deleting file because ParcelId didn't exist
        if(worked):
            f.write('%s\n%f\n%s\n%s' % (munc, acreage, city, address))
            i = i + 1
            json2019(parcelId)
            json2018(parcelId)
        else:
            print('Error with: %d' % parcelId)
            os.remove('/Users/craigglassbrenner/Desktop/WebScraping/data/html/' + 'p' + str(parcelId) + '-2019.html')
        
        # Sleeping for 1-2 seconds
        r = random.random()
        time.sleep(1 + r)

def json2019(parcelId):
            
    filepath = os.path.join('/Users/craigglassbrenner/Desktop/WebScraping/data/json2019', 'p' + str(parcelId) + '-2019.json')
    f = open(filepath, 'w+')

    params = {'ParcelID' : parcelId, 'TaxYear': '2019', 'billType' : 1}
    response = requests.get(" https://apps.lacrossecounty.org/LandRecordsPortal/services/Taxservice.svc/TaxInfoForParcel", params = params)

    try:
        mydata = response.json()
        f.write('%d\n' % mydata['ImprovementAssessedValue'])
        f.write('%d\n' % mydata['ImprovementAssessedValue'])
        f.write('%d\n' % mydata['ImprovementFairMarketValue'])
        f.write('%d\n' % mydata['LandAssessedValue'])
        f.write('%d\n' % mydata['LandFairMarketValue'])
        f.write('%d\n' % mydata['TotalAssessedValue'])
        f.write('%d\n' % mydata['TotalFairMarketValue'])

    except:
        nothing = 0
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)

    r = random.random()
    time.sleep(1 + r)

def json2018(parcelId):
            
    filepath = os.path.join('/Users/craigglassbrenner/Desktop/WebScraping/data/json2018', 'p' + str(parcelId) + '-2018.json')
    f = open(filepath, 'w+')

    params = {'ParcelID' : parcelId, 'TaxYear': '2018', 'billType' : 1}
    response = requests.get(" https://apps.lacrossecounty.org/LandRecordsPortal/services/Taxservice.svc/TaxInfoForParcel", params = params)

    try:
        mydata = response.json()
        f.write('%d\n' % mydata['ImprovementAssessedValue'])
        f.write('%d\n' % mydata['ImprovementAssessedValue'])
        f.write('%d\n' % mydata['ImprovementFairMarketValue'])
        f.write('%d\n' % mydata['LandAssessedValue'])
        f.write('%d\n' % mydata['LandFairMarketValue'])
        f.write('%d\n' % mydata['TotalAssessedValue'])
        f.write('%d\n' % mydata['TotalFairMarketValue'])

    except:
        nothing = 0
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)
        f.write('%d\n' % nothing)

    r = random.random()
    time.sleep(1 + r)

def main():
    htmlScraper()

main()








