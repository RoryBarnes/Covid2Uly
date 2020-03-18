import numpy as np
import string as str
import subprocess as subp
import csv

SourceFile=open("time_series_19-covid-Confirmed.csv","r")
UlyFile=open("covid-19.uly","w")

csvData = csv.reader(open("time_series_19-covid-Confirmed.csv","r"))
saHeader = next(csvData)
#print(saHeader[0])

iNumCols=len(saHeader)
iNumDays=iNumCols-4

print("There are "+repr(iNumDays)+" days of data.")

iaDay = [0 for i in range(iNumDays)]

for iDay in range(iNumDays):
    #print(saWords[iDay+4])
    saDate=saHeader[iDay+4].split("/")
    if int(saDate[0]) < 10:
        saDate[0] = "0"+saDate[0]
    if int(saDate[1]) < 10:
        saDate[1] = "0"+saDate[1]
    iaDay[iDay] = int(saDate[2]+saDate[0]+saDate[1])

# Find number of countries
iLine=0
iNumCountries = 0
iaCountry = [0 for i in range(300)]
saCountryTmp = ["" for i in range(300)]
for saLine in csvData:
    #print(saLine)
    bMatch = 0 # Assume the row is a new country
    sCountry=saLine[1]
    #print(sCountry)

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

saCountry = ["" for i in range(iNumCountries)]
iaConfirmed = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]

for iCountry in range(iNumCountries):
    saCountry[iCountry] = saCountryTmp[iCountry]


# Now must rest to read in cases and create proper matrix
csvData = csv.reader(open("time_series_19-covid-Confirmed.csv","r"))
saHeader = next(csvData)

#csvData.seek(0)
#saHeader = next(csvData)
print(saHeader[0])

iLine=0
iCountry = 0
iaCountry = [0 for i in range(iNumCountries)]
saCountry = ["" for i in range(iNumCountries)]
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

    # After for loop
    #if bMatch == 1:


    if bMatch == 0:
        #print(repr(iNumCountries))
        saCountry[iCountry] = sCountry
        iaCountry[iCountry] = iCountry
        #print(saCountry[iCountry],repr(iaCountry[iCountry]))
        iCountryNow = iCountry
        iCountry += 1

    #for iDay in range(iNumDays):


    for iDay in range(iNumDays):
        iaConfirmed[iCountryNow][iDay] += int(saLine[iDay+4])
        #print(repr(iaCountry[iCountry-1])+','+repr(iaDay[iDay])+','+repr(iaConfirmed[iCountry-1][iDay])+','+saCountry[iCountry-1])
    iLine += 1

sOutLine=',Country ID,Date,Confirmed Cases,#Country\n'
UlyFile.write(sOutLine)

iLine=0
for iCountry in range(iNumCountries):
    for iDay in range(iNumDays):
        iLine += 1
        sOutLine=repr(iLine)+','+repr(iaCountry[iCountry])+','+repr(iaDay[iDay])+','+repr(iaConfirmed[iCountry][iDay])+','+saCountry[iCountry]+'\n'

        UlyFile.write(sOutLine)

        #exit()
