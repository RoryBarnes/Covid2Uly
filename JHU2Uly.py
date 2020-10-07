"""

Download and convert JHU CSSE COVID-19 data in a VR Ulysses file.
Only print out the 25 countries with the most confirmed cases.

Author: Rory Barnes
Date: 8 Apr 2020

"""

import numpy as np
import string as str
import subprocess as subp
import csv
#import re
import requests
import pandas as pd

# Director and file names
sConfirmFile="time_series_covid19_confirmed_global.csv"
sDeathFile="time_series_covid19_deaths_global.csv"
urlbase="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
PopFile=open("PopulationData.csv","r")

# Get latest data
url = urlbase+sConfirmFile
r = requests.get(url, allow_redirects=False)
open(sConfirmFile,'wb').write(r.content)


url = urlbase+sDeathFile
r = requests.get(url, allow_redirects=False)
open(sDeathFile,'wb').write(r.content)

#Use cofirmed cases as a template to determine size of arrays
csvData = csv.reader(open(sConfirmFile,"r"))
saHeader = next(csvData)

iNumCols=len(saHeader)
iNumDays=iNumCols-4

print("There are "+repr(iNumDays)+" days of data.")

iaDay = [i for i in range(iNumDays)]
saDate = ["" for i in range(iNumDays)]

# Get date
for iDay in range(iNumDays):
    saDateTmp=saHeader[iDay+4].split("/")

    saDate[iDay] = saDateTmp[1]+' '

    if saDateTmp[0] == "1":
        saDate[iDay] += "Jan"
    if saDateTmp[0] == "2":
        saDate[iDay] += "Feb"
    if saDateTmp[0] == "3":
        saDate[iDay] += "Mar"
    if saDateTmp[0] == "4":
        saDate[iDay] += "Apr"
    if saDateTmp[0] == "5":
        saDate[iDay] += "May"
    if saDateTmp[0] == "6":
        saDate[iDay] += "Jun"
    if saDateTmp[0] == "7":
        saDate[iDay] += "Jul"
    if saDateTmp[0] == "8":
        saDate[iDay] += "Aug"
    if saDateTmp[0] == "9":
        saDate[iDay] += "Sep"
    if saDateTmp[0] == "10":
        saDate[iDay] += "Oct"
    if saDateTmp[0] == "11":
        saDate[iDay] += "Nov"
    if saDateTmp[0] == "12":
        saDate[iDay] += "Dec"

    saDate[iDay] += " 2020"

sToday = saDate[iNumDays-1].replace(' ','')
sOut='covid19-global-'+sToday+'.csv'
UlyFile=open(sOut,"w")
print ('Last date for data: '+sToday)

# Find number of countries
iLine=0
iNumCountries = 0
iaCountry = [0 for i in range(300)]
saCountryTmp = ["" for i in range(300)]
for saLine in csvData:
    bMatch = 0 # Assume the row is a new country
    sCountry=saLine[1]

    # Has this country been found before?
    for jLine in range(iNumCountries):
        #print(sCountry,saCountry[jLine],jLine,iNumCountries)
        if (sCountry == saCountryTmp[jLine]):
            # Match!
            #print('  Match found')
            bMatch=1
            jLine = iNumCountries # break out of loop

    # After for loop
    if bMatch == 0:
        #print(repr(iNumCountries))
        saCountryTmp[iNumCountries] = sCountry
        iNumCountries += 1

    iLine += 1

print('Total number of countries: '+repr(iNumCountries))

# Now initialize arrays
saCountry = ["" for i in range(iNumCountries)]
iaCountry = [0 for i in range(iNumCountries)]
iaMaxConfirmed = [0 for i in range(iNumCountries)]
iaConfirmed = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]
iaConfirmedDaily = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]
iaDeaths = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]
iaDeathsDaily = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]
iaPopulation = [0 for i in range(iNumCountries)]
iaCasesCapita = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]
iaDeathsCapita = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]

for iCountry in range(iNumCountries):
    saCountry[iCountry] = saCountryTmp[iCountry]

# Now must reset to read in cases a
csvData = csv.reader(open(sConfirmFile,"r"))
saHeader = next(csvData)

# Now loop through data and populate arrays
iLine=0
iCountry = 0
for saLine in csvData:
    bMatch = 0 # Assume the row is a new country
    sCountry=saLine[1]

    # Has this country been found before?
    for jLine in range(iCountry):
        #print(sCountry,saCountry[jLine],jLine,iNumCountries)
        if (sCountry == saCountry[jLine]):
            # Match!
            #print('  Match found')
            bMatch=1
            iCountryNow = iaCountry[jLine]
            jLine = iNumCountries # break out of loop

    if bMatch == 0:
        #print(repr(iNumCountries))
        saCountry[iCountry] = sCountry
        iaCountry[iCountry] = iCountry
        #print(saCountry[iCountry],repr(iaCountry[iCountry]))
        iCountryNow = iCountry
        iCountry += 1

    for iDay in range(iNumDays):
        #print(sCountry,repr(iDay),saLine[iDay+4])
        iaConfirmed[iCountryNow][iDay] += int(saLine[iDay+4])
        if iDay > 0:
            iaConfirmedDaily[iCountryNow][iDay] =  iaConfirmed[iCountryNow][iDay] - iaConfirmed[iCountryNow][iDay-1]
        else:
            iaConfirmedDaily[iCountryNow][iDay] = iaConfirmed[iCountryNow][iDay]
        if iaConfirmedDaily[iCountryNow][iDay] < 0:
            iaConfirmedDaily[iCountryNow][iDay] = 0

    iLine += 1

# Now read in deaths
csvData = csv.reader(open(sDeathFile,"r"))
saHeader = next(csvData)

iLine=0
iCountry = 0
for saLine in csvData:
    #print(saLine)
    bMatch = 0 # Assume the row is a new country
    sCountry=saLine[1]
    #print(sCountry)

    # Has this country been found before?
    for jLine in range(iCountry):
        #print(sCountry,saCountry[jLine],jLine,iNumCountries)
        if (sCountry == saCountry[jLine]):
            # Match!
            #print('  Match found')
            bMatch=1
            iCountryNow = iaCountry[jLine]
            jLine = iNumCountries # break out of loop

    if bMatch == 0:
        #print(repr(iNumCountries))
        saCountry[iCountry] = sCountry
        iaCountry[iCountry] = iCountry
        #print(saCountry[iCountry],repr(iaCountry[iCountry]))
        iCountryNow = iCountry
        iCountry += 1

    for iDay in range(iNumDays):
        iaDeaths[iCountryNow][iDay] += int(saLine[iDay+4])
        #print(sCountry,repr(iCountryNow),repr(iDay),saLine[iDay+4],repr(iaDeaths[iCountryNow][iDay]))
        #if iaConfirmed[iCountryNow][iDay] > iaMaxConfirmed[iCountryNow]:
        #    iaMaxConfirmed[iCountryNow] = iaConfirmed[iCountryNow][iDay]
        if iDay > 0:
            iaDeathsDaily[iCountryNow][iDay] =  iaDeaths[iCountryNow][iDay] - iaDeaths[iCountryNow][iDay-1]
        else:
            iaDeathsDaily[iCountryNow][iDay] = iaDeaths[iCountryNow][iDay]
        if iaDeathsDaily[iCountryNow][iDay] < 0:
            iaDeathsDaily[iCountryNow][iDay] = 0

    iLine += 1

# Read population data to calculate stats per capita
csvData = csv.reader(PopFile)
saHeader = next(csvData)
#print(saHeader[0])
for saLine in csvData:
    sCountry=saLine[0]
    iPop=int(saLine[1])
    for iCountry in range (iNumCountries):
        if saCountry[iCountry]==sCountry:
            iaPopulation[iCountry]=iPop
            for iDay in range (iNumDays):
                # Actually per million
                iaCasesCapita[iCountry][iDay]=iaConfirmed[iCountry][iDay]/iaPopulation[iCountry]*1e6
                iaDeathsCapita[iCountry][iDay]=iaDeaths[iCountry][iDay]/iaPopulation[iCountry]*1e6


# Now rank countries by total number of infections
iaWorst = [0 for i in range(iNumCountries)]

for iCountry in range(iNumCountries):
    iaWorst[iCountry] = iaConfirmed[iCountry][iNumDays-1]
    #print(saCountry[iCountry]+'\t'+repr(iaWorst[iCountry]))

# Rank countries by number of confirmed cases
iaWorst.sort(reverse=True)
#print(repr(iaWorst[24]))

# Write the file!
sOutLine=',Country ID,Days Since 22 Jan,Cumulative Cases,New Cases,Cases per Million,'
sOutLine += 'Cumulative Deaths,New Deaths,Deaths per Million,Population,'
sOutLine += '#Country,#Date\n'
UlyFile.write(sOutLine)

iLine=1
iCountryID = 0
iDaysReport = 90
for iCountry in range(iNumCountries):
    if saCountry[iCountry] == "Korea, South":
        saCountry[iCountry] = "South Korea"
    if iaConfirmed[iCountry][iNumDays-1] >= iaWorst[24]:
        for iDayIndex in range(iDaysReport):
            iDay = iNumDays + iDayIndex - iDaysReport
            sOutLine=repr(iLine)+','+repr(iCountryID)+','+repr(iaDay[iDay])+','
            sOutLine += repr(iaConfirmed[iCountry][iDay])+','+repr(iaConfirmedDaily[iCountry][iDay])+','+repr(iaCasesCapita[iCountry][iDay])+','
            sOutLine += repr(iaDeaths[iCountry][iDay])+','+repr(iaDeathsDaily[iCountry][iDay])+','+repr(iaDeathsCapita[iCountry][iDay])+','
            sOutLine += repr(iaPopulation[iCountry])+','+saCountry[iCountry]+','+saDate[iDay]+'\n'
            UlyFile.write(sOutLine)
            iLine += 1

        #print(repr(iCountryID))
        iCountryID += 1
        #exit()

# Copy file into US.csv
UlyFile.close()
cmd = "cp "+sOut+" global.csv"
subp.call(cmd,shell=True)
