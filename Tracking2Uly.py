"""

Download and convert COVID Trackin Project COVID-19 data in a VR Ulysses file.

Author: Rory Barnes
Date: 8 Apr 2020

"""

import numpy as np
import string as str
import subprocess as subp
import csv
import subprocess as subp
import re
import requests
import pandas as pd

sDirCovidTracking="/Users/rory/DataViz/Ulysses/covid19/covid-tracking-data/data"
#sSource="/Users/rory/DataViz/Ulysses/covid19/covid-tracking-data/data/states_daily_4pm_et.csv"
sSource="daily.csv"

iDaysJan=9
iDaysFeb=29
iDaysMarch=31
iDaysApril=30
iDaysMay=31
iDaysJune=30
iDaysJuly=31
iDaysAug=31
iDaysSep=30
iDaysOct=31
iDaysNov=30
iDaysDec=31

# Return number of days, and date
def fnDays(sDate):
    iYear=int(sDate[0:4])
    iMonth=int(sDate[4:6])
    iDay=int(sDate[-2:])
    # Sometime I'll make this more elegant
    if iMonth == 1:
        iNumDays = iDay - 22
    if iMonth == 2:
        iNumDays = iDay + iDaysJan
    if iMonth == 3:
        iNumDays = iDay + iDaysJan + iDaysFeb
    if iMonth == 4:
        iNumDays = iDay + iDaysJan + iDaysFeb + iDaysMarch
    if iMonth == 5:
        iNumDays = iDay + iDaysApril + iDaysMarch + iDaysJan + iDaysFeb
    if iMonth == 6:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysMarch + iDaysJan + iDaysFeb
    if iMonth == 7:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysMarch + iDaysJan + iDaysFeb
    if iMonth == 8:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysJuly + iDaysMarch + iDaysJan + iDaysFeb
    if iMonth == 9:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysJuly + iDaysAug + iDaysMarch + iDaysJan + iDaysFeb
    if iMonth == 10:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysJuly + iDaysAug + iDaysMarch + iDaysJan + iDaysFeb + iDaysSep
    if iMonth == 11:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysJuly + iDaysAug + iDaysMarch + iDaysJan + iDaysFeb + iDaysSep + iDaysOct
    if iMonth == 12:
        iNumDays = iDay + iDaysApril + iDaysMay + iDaysJune + iDaysJuly + iDaysAug + iDaysMarch + iDaysJan + iDaysFeb + iDaysSep + iDaysOct + iDaysNov

    # First day still counts
    #print(repr(iDay),repr(iMonth),sDate)
    iNumDays += 1
    sDate=repr(iDay)+' '
    if iMonth == 1:
        sDate += 'Jan'
    if iMonth == 2:
        sDate += 'Feb'
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
    if iMonth == 9:
        sDate += "Sep"
    if iMonth == 10:
        sDate += "Oct"
    if iMonth == 11:
        sDate += "Nov"
    if iMonth == 12:
        sDate += "Dec"

    sDate += ' 2020'
    #print (sDate)
    return iNumDays,sDate

# Return iState,sState,iPopulation (from Wikipedia)
def fnState(sAbbrev):
    if sAbbrev == "AK":
        return 0,"Alaska",0.732
    if sAbbrev == "AL":
        return 1,"Alabama",4.903
    if sAbbrev == "AR":
        return 2,"Arkansas",3.018
    if sAbbrev == "AS":
        return 3,"American Samoa",0.056
    if sAbbrev == "AZ":
        return 4,"Arizona",7.279
    if sAbbrev == "CA":
        return 5,"California",39.512
    if sAbbrev == "CO":
        return 6,"Colorado",5.729
    if sAbbrev == "CT":
        return 7,"Connecticut",3.565
    if sAbbrev == "DC":
        return 8,"District of Columbia",0.706
    if sAbbrev == "DE":
        return 9,"Delaware",0.974
    if sAbbrev == "FL":
        return 10,"Florida",21.478
    if sAbbrev == "GA":
        return 11,"Georgia",10.617
    if sAbbrev == "GU":
        return 12,"Guam",0.166
    if sAbbrev == "HI":
        return 13,"Hawaii",1.416
    if sAbbrev == "IA":
        return 14,"Iowa",3.155
    if sAbbrev == "ID":
        return 15,"Idaho",1.787
    if sAbbrev == "IL":
        return 16,"Illinois",12.671
    if sAbbrev == "IN":
        return 17,"Indiana",6.732
    if sAbbrev == "KS":
        return 18,"Kansas",2.913
    if sAbbrev == "KY":
        return 19,"Kentucky",4.468
    if sAbbrev == "LA":
        return 20,"Louisiana",4.649
    if sAbbrev == "MA":
        return 21,"Massachusetts",6.950
    if sAbbrev == "MD":
        return 22,"Maryland",6.046
    if sAbbrev == "ME":
        return 23,"Maine",1.344
    if sAbbrev == "MI":
        return 24,"Michigan",9.987
    if sAbbrev == "MN":
        return 25,"Minnesota",5.640
    if sAbbrev == "MO":
        return 26,"Missourri",6.137
    if sAbbrev == "MP":
        return 27,"Northern Mariana Islands",0.055
    if sAbbrev == "MS":
        return 28,"Mississippi",2.976
    if sAbbrev == "MT":
        return 29,"Montana",1.069
    if sAbbrev == "NC":
        return 30,"North Carolina",10.488
    if sAbbrev == "ND":
        return 31,"North Dakota",0.762
    if sAbbrev == "NE":
        return 32,"Nebraska",1.934
    if sAbbrev == "NH":
        return 33,"New Hampshire",1.360
    if sAbbrev == "NJ":
        return 34,"New Jersey",8.882
    if sAbbrev == "NM":
        return 35,"New Mexico",2.097
    if sAbbrev == "NV":
        return 36,"Nevada",3.080
    if sAbbrev == "NY":
        return 37,"New York",19.454
    if sAbbrev == "OH":
        return 38,"Ohio",11.689
    if sAbbrev == "OK":
        return 39,"Oklahoma",3.957
    if sAbbrev == "OR":
        return 40,"Oregon",4.218
    if sAbbrev == "PA":
        return 41,"Pennsylvania",12.802
    if sAbbrev == "PR":
        return 42,"Puerto Rico",3.194
    if sAbbrev == "RI":
        return 43,"Rhode Island",1.059
    if sAbbrev == "SC":
        return 44,"South Carolina",5.149
    if sAbbrev == "SD":
        return 45,"South Dakota",0.885
    if sAbbrev == "TN":
        return 46,"Tennessee",6.833
    if sAbbrev == "TX":
        return 47,"Texas",28.996
    if sAbbrev == "UT":
        return 48,"Utah",3.206
    if sAbbrev == "VA":
        return 49,"Virginia",8.536
    if sAbbrev == "VI":
        return 50,"Virgin Islands",0.105
    if sAbbrev == "VT":
        return 51,"Vermont",0.624
    if sAbbrev == "WA":
        return 52,"Washington",7.615
    if sAbbrev == "WI":
        return 53,"Wisconsin",5.822
    if sAbbrev == "WV":
        return 54,"West Virginia",1.792
    if sAbbrev == "WY":
        return 55,"Wyoming",0.579

iNumStates = 56

# Get latest data
#sCmd = 'cd '+sDirCovidTracking+'; git pull origin master >& gitlog'
#sCmd = 'cd '+sDirCovidTracking


# Cut for debugging
url = 'https://covidtracking.com/api/v1/states/daily.csv'
r = requests.get(url, allow_redirects=True)
open('daily.csv','wb').write(r.content)

#sCmd = `mv daily.csv `+sDirCovidTracking
#subp.call(sCmd, shell=True)

#exit()
print('Latest data set downloaded.')

"""
To initialize columns, must get total number of days in latest data set. The
code reads in the first 2 lines of the file and computes the number of days
since 04 Mar 2020, the first date in the data set. After initializing the
matrices, the file stream is reset, the header read in again, and then the loop
to read in the numeric data is executed.
"""

"""
Column header of the COVID-19 Tracking data

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
DataQuality,12
lasUpdate,13
dateModified,14
checkTime,15
death,16
hospitalized,17
dateChecked,18
fips,19
positiveIncrease,20
negativeIncrease,21
totalTestResultsIncrease,22
posNeg,23
deathIncrease,24
hospitalizedIncrease,25
hash,26
commericalScore,27
negRegularScore,28
negativeScore,29
positiveScore,30
score,31
grade,32
"""

# Read in data as Pandas Dataframe
data = pd.read_csv(sSource)
# Fill in missing values with 0
data.fillna(0, inplace=True)
# Convert relevant columns to ints
data['death'] = data['death'].astype(int)
data['hospitalizedCumulative'] = data['hospitalizedCumulative'].astype(int)
data['hospitalizedCurrently'] = data['hospitalizedCurrently'].astype(int)
data['inIcuCumulative'] = data['inIcuCumulative'].astype(int)
data['inIcuCurrently'] = data['inIcuCurrently'].astype(int)
data['negative'] = data['negative'].astype(int)
data['onVentilatorCumulative'] = data['onVentilatorCumulative'].astype(int)
data['onVentilatorCurrently'] = data['onVentilatorCurrently'].astype(int)
data['pending'] = data['pending'].astype(int)
data['positive'] = data['positive'].astype(int)
data['recovered'] = data['recovered'].astype(int)

iaDate = data['date'].values
iaDeathsTotal = data['death'].values
iaHospitalizedCumulative = data['hospitalizedCumulative'].values
iaHospitalizedCurrently = data['hospitalizedCurrently'].values
iaInIcuCumulative = data['inIcuCumulative'].values
iaInIcuCurrently = data['inIcuCurrently'].values
iaNegativeCumulative = data['negative'].values
iaOnVentilatorCumulative = data['onVentilatorCumulative'].values
iaOnVentilatorCurrently = data['onVentilatorCurrently'].values
iaPending = data['pending'].values
iaPositiveCumulative = data['positive'].values
iaRecoveredCumulative = data['recovered'].values

saDataQuality = data['dataQualityGrade'].values
saFIPS = data['fips'].values
saHash = data['hash'].values
saLastUpdate = data['lastUpdateEt'].values
saState = data['state'].values

iRows = len (data['date'].values)

iNumDays,sFoo = fnDays(repr(iaDate[0]))

print('Found '+repr(iNumDays)+' days of data.')

iaPositive = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaNegative = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaPend = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
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
daPercentPos = [[0.0 for i in range(iNumDays)] for j in range(iNumStates)]
iaDeathsMillion = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaPosMillion = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaTestsMillion = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaTestsCumulative = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
saAbbrev = ["" for i in range(iNumStates)]
iaPop = [0 for i in range(iNumStates)]
saDate = ["" for i in range(iNumDays)]

for iRow in range(iRows):
    #sAbbrev=saLine[1]
    # Must convert to days since 22 Jan
    iDaysSince22Jan,sDateNew = fnDays(repr(iaDate[iRow]))
    #print(sDate+' '+repr(iDaysSince04Mar))
    saDate[iDaysSince22Jan-1] = sDateNew
    #print(repr(iDaysSince22Jan))
    #print(saState[iRow])
    iState,sState,iPopulation = fnState(saState[iRow])
    saAbbrev[iState] = sState
    iaPop[iState] = iPopulation

    iaPositive[iState][iDaysSince22Jan-1] = iaPositiveCumulative[iRow]
    iaNegative[iState][iDaysSince22Jan-1] = iaNegativeCumulative[iRow]
    iaPend[iState][iDaysSince22Jan-1] = iaPending[iRow]
    iaHospCur[iState][iDaysSince22Jan-1] = iaHospitalizedCurrently[iRow]
    iaHospCum[iState][iDaysSince22Jan-1] = iaHospitalizedCumulative[iRow]
    iaICUCur[iState][iDaysSince22Jan-1] = iaInIcuCurrently[iRow]
    iaICUCum[iState][iDaysSince22Jan-1] = iaInIcuCumulative[iRow]
    iaVentCur[iState][iDaysSince22Jan-1] = iaOnVentilatorCurrently[iRow]
    iaVentCum[iState][iDaysSince22Jan-1] = iaOnVentilatorCumulative[iRow]
    iaRecovered[iState][iDaysSince22Jan-1] = iaRecoveredCumulative[iRow]
    iaDeaths[iState][iDaysSince22Jan-1] = iaDeathsTotal[iRow]

for iState in range(iNumStates):
    for iDay in range(iNumDays):
        if iDay > 0:
            iaDeathsNew[iState][iDay] = iaDeaths[iState][iDay] - iaDeaths[iState][iDay-1]
            iaHospNew[iState][iDay] = iaHospCum[iState][iDay] - iaHospCur[iState][iDay]
            iaPosNew[iState][iDay] = iaPositive[iState][iDay] - iaPositive[iState][iDay-1]
            iaTestsNew[iState][iDay] = iaTestsCumulative[iState][iDay] - iaTestsCumulative[iState][iDay-1]
        else:
            iaDeathsNew[iState][iDay] = 0
            iaHospNew[iState][iDay] = 0
            iaPosNew[iState][iDay] = 0
            iaTestsCumulative[iState][iDay] = iaPositive[iState][iDay] + iaNegative[iState][iDay] + iaPend[iState][iDay]
        iaDeathsMillion[iState][iDay] = iaDeaths[iState][iDay]/iaPop[iState]
        iaPosMillion[iState][iDay] = iaPositive[iState][iDay]/iaPop[iState]
        iaTestsMillion[iState][iDay] = iaTests[iState][iDay]/iaPop[iState]
        if iaTestsNew[iState][iDaysSince22Jan-1] > 0:
            #print("% Pos > 0")
            daPercentPos[iState][iDay] = float(iaPosNew[iState][iDay])/iaTestsNew[iState][iDay]
            #print(repr(iaPosNew[iState][iDaysSince22Jan-1]), repr(iaTestsNew[iState][iDaysSince22Jan-1]), repr(daPercentPos[iState][iDaysSince22Jan-1]))
        else:
            daPercentPos[iState][iDaysSince22Jan-1] = 0.0

print ('Last date for data: '+saDate[-1])


"""
csvData = csv.reader(open(sSource,"r"))
saHeader = next(csvData)

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
daPercentPos = [[0.0 for i in range(iNumDays)] for j in range(iNumStates)]
iaDeathsMillion = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaPosMillion = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
iaTestsMillion = [[0 for i in range(iNumDays)] for j in range(iNumStates)]
saState = ["" for i in range(iNumStates)]
iaPop = [0 for i in range(iNumStates)]
saDate = ["" for i in range(iNumDays)]

# Rest csv file and read in header
csvData = csv.reader(open(sSource,"r"))
saHeader = next(csvData)

for saLine in csvData:
    sDate=saLine[0]
    sAbbrev=saLine[1]
    # Must convert to days since March 4th
    iDaysSince22Jan,sDateNew = fnDays(sDate)
    #print(sDate+' '+repr(iDaysSince04Mar))
    saDate[iDaysSince22Jan-1] = sDateNew
    #print(repr(iDaysSince22Jan))
    iState,sState,iPopulation = fnState(sAbbrev)
    saState[iState] = sState
    iaPop[iState] = iPopulation
    #print(sState,repr(iState),repr(iDaysSince22Jan))
    if saLine[2] != '':
        iaPositive[iState][iDaysSince22Jan-1] = int(saLine[2])
    if saLine[3] != '':
        iaNegative[iState][iDaysSince22Jan-1] = int(saLine[3])
    if saLine[4] != '':
        iaPending[iState][iDaysSince22Jan-1] = int(saLine[4])
    if saLine[5] != '':
        iaHospCur[iState][iDaysSince22Jan-1] = int(saLine[5])
    if saLine[6] != '':
        iaHospCum[iState][iDaysSince22Jan-1] = int(saLine[6])
    if saLine[7] != '':
        iaICUCur[iState][iDaysSince22Jan-1] = int(saLine[7])
    if saLine[8] != '':
        iaICUCum[iState][iDaysSince22Jan-1] = int(saLine[8])
    if saLine[9] != '':
        iaVentCur[iState][iDaysSince22Jan-1] = int(saLine[9])
    if saLine[10] != '':
        iaVentCum[iState][iDaysSince22Jan-1] = int(saLine[10])
    if saLine[11] != '':
        iaRecovered[iState][iDaysSince22Jan-1] = int(saLine[11])
    if saLine[16] != '':
        iaDeaths[iState][iDaysSince22Jan-1] = int(saLine[16])
    if saLine[19] != '':
        iaTests[iState][iDaysSince22Jan-1] = int(saLine[19])
    if saLine[22] != '':
        iaDeathsNew[iState][iDaysSince22Jan-1] = int(saLine[22])
    if saLine[23] != '':
        iaHospNew[iState][iDaysSince22Jan-1] = int(saLine[23])
    if saLine[24] != '':
        iaNegNew[iState][iDaysSince22Jan-1] = int(saLine[24])
    if saLine[25] != '':
        iaPosNew[iState][iDaysSince22Jan-1] = int(saLine[25])
    if saLine[26] != '':
        iaTestsNew[iState][iDaysSince22Jan-1] = int(saLine[26])
"""

# Read in with Pandas data frame

"""
    if iaTestsNew[iState][iDaysSince22Jan-1] > 0:
        #print("% Pos > 0")
        daPercentPos[iState][iDaysSince22Jan-1] = float(iaPosNew[iState][iDaysSince22Jan-1])/iaTestsNew[iState][iDaysSince22Jan-1]
        #print(repr(iaPosNew[iState][iDaysSince22Jan-1]), repr(iaTestsNew[iState][iDaysSince22Jan-1]), repr(daPercentPos[iState][iDaysSince22Jan-1]))
    else:
        daPercentPos[iState][iDaysSince22Jan-1] = 0.0


    #print(repr(daPercentPos[iState][iDaysSince22Jan-1]))
    iaDeathsMillion[iState][iDaysSince22Jan-1] = iaDeaths[iState][iDaysSince22Jan-1]/iaPop[iState]
    iaPosMillion[iState][iDaysSince22Jan-1] = iaPositive[iState][iDaysSince22Jan-1]/iaPop[iState]
    iaTestsMillion[iState][iDaysSince22Jan-1] = iaTests[iState][iDaysSince22Jan-1]/iaPop[iState]
"""

# Write data!
sOut='covid19-US-'+saDate[-1].replace(" ", "") +'.csv'
#print ('Last date for data: '+saDate[-1])
OutFile=open(sOut,'w')

sOutLine=',State ID,Days Since Jan 22,'
sOutLine += 'Cumulative Deaths,New Deaths,'
sOutLine += 'Cumulative Positive,New Positive,% Positive,'
sOutLine += 'Cumulative Tests,New Tests,'
sOutLine += 'Cumulative Hospitalized,Current Hospitalized,New Hospitalized,'
sOutLine += 'Cumulative in ICU,Currently in ICU,'
sOutLine += 'Cumulative on Vent.,Currently on Vent.,'
sOutLine += 'Deaths/Million,Pos./Million,Tests/Million,'
sOutLine += 'Population,'
sOutLine += '#State,#Date\n'

OutFile.write(sOutLine)

iID = 1
#iLines =3000
iDaysReport = 45
for iState in range(iNumStates):
#    for iDayIndex in range(iLines):
#        iDay = iID + iDayIndex - iLines
#    for iDay in range(iNumDays):
    for iDayIndex in range(iDaysReport):
        iDay = iNumDays + iDayIndex - iDaysReport
        sOutLine = repr(iID)+','+repr(iState)+','+repr(iDay)+','
        sOutLine += repr(iaDeaths[iState][iDay])+','+repr(iaDeathsNew[iState][iDay])+','
        sOutLine += repr(iaPositive[iState][iDay])+','+repr(iaPosNew[iState][iDay])+','+repr(daPercentPos[iState][iDay])+','
        sOutLine += repr(iaTests[iState][iDay])+','+repr(iaTestsNew[iState][iDay])+','
        sOutLine += repr(iaHospCum[iState][iDay])+','+repr(iaHospCur[iState][iDay])+','+repr(iaHospNew[iState][iDay])+','
        sOutLine += repr(iaICUCum[iState][iDay])+','+repr(iaICUCur[iState][iDay])+','
        sOutLine += repr(iaVentCum[iState][iDay])+','+repr(iaVentCur[iState][iDay])+','
        sOutLine += repr(iaDeathsMillion[iState][iDay])+','+repr(iaPosMillion[iState][iDay])+','+repr(iaTestsMillion[iState][iDay])+','
        sOutLine += repr(iaPop[iState])+','
        sOutLine += saState[iState]+','+saDate[iDay]+'\n'
        OutFile.write(sOutLine)
        iID += 1

# Copy file into US.csv
OutFile.close()
cmd = "cp "+sOut+" US.csv"
subp.call(cmd,shell=True)
exit(0)
