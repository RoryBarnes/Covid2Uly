import numpy as np
import string as str
import subprocess as subp
import csv
import subprocess as subp
import re

sDirCovidTracking="/Users/rory/DataViz/Ulysses/covid19/covid-tracking-data/data"
sSource="/Users/rory/DataViz/Ulysses/covid19/covid-tracking-data/data/states_daily_4pm_et.csv"

iDaysMarch=27
iDaysApril=30
iDaysMay=31
iDaysJune=30
iDaysJuly=31
iDaysAug=31

def fnDays(sDate):
    iYear=int(sDate[0:4])
    iMonth=int(sDate[4:6])
    iDay=int(sDate[-2:])
    if iMonth == 3:
        iNumDays = iDay - 4
    if iMonth == 4:
        iNumDays = iDay + iDaysMarch
    if iMonth == 5:
        iNumDays = iDay + iDaysApril + iDaysMarch
    if iMonth == 6:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysMarch
    if iMonth == 7:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysMarch
    if iMonth == 8:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysJuly + iDaysMarch
    if iMonth == 9:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysJuly + iDaysAug + iDaysMarch

    # First day still counts
    iNumDays += 1
    sDate=repr(iDay)+' '
    if iMonth == 3:
        sDate += 'Mar'
    if iMonth == 4:
        sDate += 'Apr'
    if iMonth == 5:
        sDate += 'May'
    if iMonth == 6:
        sDate += 'Jun'
    if iMonth == 7:
        sDate += 'Jul'
    if iMonth == 8:
        sDate += 'Aug'

    sDate += ' 2020'
    return iNumDays,sDate

def fnState(sAbbrev):
    # iState,sState,iPopulation
    if sAbbrev == "AK":
        return 0,"Alaska"
    if sAbbrev == "AL":
        return 1,"Alabama"
    if sAbbrev == "AR":
        return 2,"Arkansas"
    if sAbbrev == "AS":
        return 3,"American Samoa"
    if sAbbrev == "AZ":
        return 4,"Arizona"
    if sAbbrev == "CA":
        return 5,"California"
    if sAbbrev == "CO":
        return 6,"Colorado"
    if sAbbrev == "CT":
        return 7,"Connecticut"
    if sAbbrev == "DC":
        return 8,"District of Columbia"
    if sAbbrev == "DE":
        return 9,"Delaware"
    if sAbbrev == "FL":
        return 10,"Florida"
    if sAbbrev == "GA":
        return 11,"Georgia"
    if sAbbrev == "GU":
        return 12,"Guam"
    if sAbbrev == "HI":
        return 13,"Hawaii"
    if sAbbrev == "IA":
        return 14,"Iowa"
    if sAbbrev == "ID":
        return 15,"Idaho"
    if sAbbrev == "IL":
        return 16,"Illinois"
    if sAbbrev == "IN":
        return 17,"Indiana"
    if sAbbrev == "KS":
        return 18,"Kansas"
    if sAbbrev == "KY":
        return 19,"Kentucky"
    if sAbbrev == "LA":
        return 20,"Louisiana"
    if sAbbrev == "MA":
        return 21,"Massachusetts"
    if sAbbrev == "MD":
        return 22,"Maryland"
    if sAbbrev == "ME":
        return 23,"Maine"
    if sAbbrev == "MI":
        return 24,"Michigan"
    if sAbbrev == "MN":
        return 25,"Minnesota"
    if sAbbrev == "MO":
        return 26,"Missourri"
    if sAbbrev == "MP":
        return 27,"Northern Mariana Islands"
    if sAbbrev == "MS":
        return 28,"Mississippi"
    if sAbbrev == "MT":
        return 29,"Montana"
    if sAbbrev == "NC":
        return 30,"North Carolina"
    if sAbbrev == "ND":
        return 31,"North Dakota"
    if sAbbrev == "NE":
        return 32,"Nebraska"
    if sAbbrev == "NH":
        return 33,"New Hampshire"
    if sAbbrev == "NJ":
        return 34,"New Jersey"
    if sAbbrev == "NM":
        return 35,"New Mexico"
    if sAbbrev == "NV":
        return 36,"Nevada"
    if sAbbrev == "NY":
        return 37,"New York"
    if sAbbrev == "OH":
        return 38,"Ohio"
    if sAbbrev == "OK":
        return 39,"Oklahoma"
    if sAbbrev == "OR":
        return 40,"Oregon"
    if sAbbrev == "PA":
        return 41,"Pennsylvania"
    if sAbbrev == "PR":
        return 42,"Puerto Rico"
    if sAbbrev == "RI":
        return 43,"Rhode Island"
    if sAbbrev == "SC":
        return 44,"South Carolina"
    if sAbbrev == "SD":
        return 45,"South Dakota"
    if sAbbrev == "TN":
        return 46,"Tennessee"
    if sAbbrev == "TX":
        return 47,"Texas"
    if sAbbrev == "UT":
        return 48,"Utah"
    if sAbbrev == "VA":
        return 49,"Virginia"
    if sAbbrev == "VI":
        return 50,"Virgin Islands"
    if sAbbrev == "VT":
        return 51,"Vermont"
    if sAbbrev == "WA":
        return 52,"Washington"
    if sAbbrev == "WI":
        return 53,"Wisconsin"
    if sAbbrev == "WV":
        return 54,"West Virginia"
    if sAbbrev == "WY":
        return 55,"Wyoming"

iNumStates = 56
#iNumDays = 27

# Get latest data
sCmd = 'cd '+sDirCovidTracking+'; git pull origin master >& gitlog'
#print (sCmd)
subp.call(sCmd, shell=True)

print('Latest data set downloaded.')


"""
To initialize columns, must get total number of days in latest data set. The
code reads in the first 2 lines of the file and computes the number of days
since 04 Mar 2020, the first date in the data set. After initializing the
matrices, the file stream is reset, the header read in again, and then the loop
to read in the numeric data is executed.
"""

"""
Column header of teh COVID-19 Tracking data

date,0
state,1
positive,2
negative,3
pending,4
hospitalizedCurrently,5
hospitalizedCumulative,6
inIcuCurrently,7
inIcuCumulative,8
onVentilatorCurrently,9
onVentilatorCumulative,10
recovered,11
hash,12
dateChecked,13
death,14
hospitalized,15
total,16
totalTestResults,17
posNeg,18
fips,19
deathIncrease,20
hospitalizedIncrease,21
negativeIncrease,22
positiveIncrease,23
totalTestResultsIncrease,24
"""

csvData = csv.reader(open(sSource,"r"))
saHeader = next(csvData)
#print(saHeader[0],saHeader[5])

saLine = next(csvData)
sDate=saLine[0]
sAbbrev=saLine[1]
# Must convert to days since March 4th
iNumDays,sFoo = fnDays(sDate)
print('Found '+repr(iNumDays)+' days of data.')

iaPositive = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaNegative = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaPending = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaHospCur = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaHospCum = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaICUCur = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaICUCum = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaVentCum = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaVentCur = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaDeaths = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaTests = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaRecovered = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaDeathsNew = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaHospNew = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaNegNew = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaPosNew = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaTestsNew = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaPercentPos = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
saState = ["" for i in range(iNumStates)]
saDate = ["" for i in range(iNumDays)]

# Rest csv file and read in header
csvData = csv.reader(open(sSource,"r"))
saHeader = next(csvData)

for saLine in csvData:
    sDate=saLine[0]
    sAbbrev=saLine[1]
    # Must convert to days since March 4th
    iDaysSince04Mar,sDateNew = fnDays(sDate)
    #print(sDate+' '+repr(iDaysSince04Mar))
    saDate[iDaysSince04Mar-1] = sDateNew
    #print(repr(iDaysSince04Mar))
    iState,sState = fnState(sAbbrev)
    saState[iState] = sState
    #print(sState,repr(iState),repr(iDaysSince04Mar))
    if saLine[2] != '':
        iaPositive[iState][iDaysSince04Mar-1] = int(saLine[2])
    if saLine[3] != '':
        iaNegative[iState][iDaysSince04Mar-1] = int(saLine[3])
    if saLine[4] != '':
        iaPending[iState][iDaysSince04Mar-1] = int(saLine[4])
    if saLine[5] != '':
        iaHospCur[iState][iDaysSince04Mar-1] = int(saLine[5])
    if saLine[6] != '':
        iaHospCum[iState][iDaysSince04Mar-1] = int(saLine[6])
    if saLine[7] != '':
        iaICUCur[iState][iDaysSince04Mar-1] = int(saLine[7])
    if saLine[8] != '':
        iaICUCum[iState][iDaysSince04Mar-1] = int(saLine[8])
    if saLine[9] != '':
        iaVentCur[iState][iDaysSince04Mar-1] = int(saLine[9])
    if saLine[10] != '':
        iaVentCum[iState][iDaysSince04Mar-1] = int(saLine[10])
    if saLine[11] != '':
        iaRecovered[iState][iDaysSince04Mar-1] = int(saLine[11])
    if saLine[14] != '':
        iaDeaths[iState][iDaysSince04Mar-1] = int(saLine[14])
    if saLine[17] != '':
        iaTests[iState][iDaysSince04Mar-1] = int(saLine[17])
    if saLine[20] != '':
        iaDeathsNew[iState][iDaysSince04Mar-1] = int(saLine[20])
    if saLine[21] != '':
        iaHospNew[iState][iDaysSince04Mar-1] = int(saLine[21])
    if saLine[22] != '':
        iaNegNew[iState][iDaysSince04Mar-1] = int(saLine[22])
    if saLine[23] != '':
        iaPosNew[iState][iDaysSince04Mar-1] = int(saLine[23])
    if saLine[24] != '':
        iaTestsNew[iState][iDaysSince04Mar-1] = int(saLine[24])

    if iaTestsNew[iState][iDaysSince04Mar-1] > 0:
        iaPercentPos[iState][iDaysSince04Mar-1] = iaPosNew[iState][iDaysSince04Mar-1]/iaTestsNew[iState][iDaysSince04Mar-1]
    else:
        iaPercentPos[iState][iDaysSince04Mar-1] = 0

sOut='covid19-US-'+saDate[-1].replace(" ", "") +'.csv'
OutFile=open(sOut,'w')

sOutLine=',State ID,Days Since Mar 3,'
sOutLine += 'Cumulative Deaths,New Deaths,'
sOutLine += 'Cumulative Positive,New Positive,\% Positive,'
sOutLine += 'Cumulative Tests,New Tests,Recovered,'
sOutLine += 'Cumulative Hospitalized,Current Hospitalized,New Hospitalized,'
sOutLine += 'Cumulative in ICU,Currently in ICU,'
sOutLine += 'Cumulative on Vent.,Currently on Vent.'
sOutLine += '#State,#Date,'
sOutLine += 'NULL\n'

OutFile.write(sOutLine)

iID = 0
for iState in range(iNumStates):
    for iDay in range(iNumDays):
        sOutLine = repr(iID)+','+repr(iState)+','+repr(iDay)+','
        sOutLine += repr(iaDeaths[iState][iDay])+','+repr(iaDeathsNew[iState][iDay])+','
        sOutLine += repr(iaPositive[iState][iDay])+','+repr(iaPosNew[iState][iDay])+','+repr(iaPercentPos[iState][iDaysSince04Mar-1])+','
        sOutLine += repr(iaTests[iState][iDay])+','+repr(iaTestsNew[iState][iDay])+','+repr(iaRecovered[iState][iDaysSince04Mar-1])+','
        sOutLine += repr(iaHospCum[iState][iDay])+','+repr(iaHospCur[iState][iDay])+','+repr(iaHospNew[iState][iDay])+','
        sOutLine += repr(iaICUCum[iState][iDay])+','+repr(iaICUCur[iState][iDay])+','
        sOutLine += repr(iaVentCum[iState][iDay])+','+repr(iaVentCur[iState][iDay])+','
        #print(repr(iDay)+'  '+saDate[iDay])
        sOutLine += saState[iState]+','+saDate[iDay]+',-1\n'
        OutFile.write(sOutLine)
        iID += 1

exit(0)
