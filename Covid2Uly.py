import numpy as np
import string as str
import subprocess as subp
import csv
import subprocess as subp

sCSSEDir="/Users/rory/DataViz/Ulysses/covid19/COVID-19/"
sSourceFile=sCSSEDir+"csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
UlyFile=open("covid-19.uly","w")
PopFile=open("PopulationData.csv","r")

# Get latest data
sCmd = 'cd '+sCSSEDir+'; git pull origin master >& gitlog'
#print (sCmd)
subp.call(sCmd, shell=True)

csvData = csv.reader(open(sSourceFile,"r"))
saHeader = next(csvData)
#print(saHeader[0])

iNumCols=len(saHeader)
iNumDays=iNumCols-4

print("There are "+repr(iNumDays)+" days of data.")

iaDay = [i for i in range(iNumDays)]
saDate = ["" for i in range(iNumDays)]

# Get date
for iDay in range(iNumDays):
    #print(saWords[iDay+4])
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
        saDate[iDay] += "JDec"

    saDate[iDay] += " 2020"

sToday = saDate[iNumDays-1].replace(' ','')
#sOutFileName =
UlyFile=open('covid19-'+sToday+'.uly',"w")
#print (sToday)

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
iaCountry = [0 for i in range(iNumCountries)]
iaMaxConfirmed = [0 for i in range(iNumCountries)]
iaConfirmed = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]
iaConfirmedDaily = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]
iaPopulation = [0 for i in range(iNumCountries)]
iaCasesCapita = [[0 for i in range(iNumDays)] for j in range(iNumCountries)]

for iCountry in range(iNumCountries):
    saCountry[iCountry] = saCountryTmp[iCountry]


# Now must reset to read in cases and create proper matrix
csvData = csv.reader(open(sSourceFile,"r"))
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

    #for iDay in range(iNumDays):


    for iDay in range(iNumDays):
        #print(sCountry,repr(iDay),saLine[iDay+4])
        iaConfirmed[iCountryNow][iDay] += int(saLine[iDay+4])
        #if iaConfirmed[iCountryNow][iDay] > iaMaxConfirmed[iCountryNow]:
        #    iaMaxConfirmed[iCountryNow] = iaConfirmed[iCountryNow][iDay]
        if iDay > 0:
            iaConfirmedDaily[iCountryNow][iDay] =  iaConfirmed[iCountryNow][iDay] - iaConfirmed[iCountryNow][iDay-1]
        else:
            iaConfirmedDaily[iCountryNow][iDay] = iaConfirmed[iCountryNow][iDay]
        if iaConfirmedDaily[iCountryNow][iDay] < 0:
            iaConfirmedDaily[iCountryNow][iDay] = 0

    iLine += 1

#print("Country\tMaxC")
#for iCountry in range(iNumCountries):

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
                iaCasesCapita[iCountry][iDay]=iaConfirmed[iCountry][iDay]/iaPopulation[iCountry]*1e6

# Now rank countries by total number of infections
iaWorst = [0 for i in range(iNumCountries)]

for iCountry in range(iNumCountries):
    iaWorst[iCountry] = iaConfirmed[iCountry][iNumDays-1]
    #print(saCountry[iCountry]+'\t'+repr(iaWorst[iCountry]))

iaWorst.sort(reverse=True)
#print(repr(iaWorst[24]))
#for iCountry in range(iNumCountries):
    #iaWorst[iCountry] = iaConfirmed[iCountry][iNumDays-1]
    #print(saCountry[iCountry]+'\t'+repr(iaWorst[iCountry]))


sOutLine=',Country ID,Days Since 22 Jan,Cumulative Cases,New Cases,Cases per Million,Population,#Country,#Date,NULL\n'
UlyFile.write(sOutLine)

iLine=0
iCountryID = 0
for iCountry in range(iNumCountries):
    if saCountry[iCountry] == "Korea, South":
        saCountry[iCountry] = "South Korea"
    if iaConfirmed[iCountry][iNumDays-1] >= iaWorst[24]:
        for iDay in range(iNumDays):
            sOutLine=repr(iLine)+','+repr(iCountryID)+','+repr(iaDay[iDay])+','+repr(iaConfirmed[iCountry][iDay])
            sOutLine += ','+repr(iaConfirmedDaily[iCountry][iDay])+','+repr(iaCasesCapita[iCountry][iDay])
            sOutLine += ','+repr(iaPopulation[iCountry])+','+saCountry[iCountry]+','+saDate[iDay]+',-1\n'
            UlyFile.write(sOutLine)
            iLine += 1

        #print(repr(iCountryID))
        iCountryID += 1
        #exit()
