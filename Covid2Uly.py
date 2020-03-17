import numpy as np
import string as str
import subprocess as subp

SourceFile=open("time_series_19-covid-Confirmed.csv","r")
UlyFile=open("covid-19.uly","w")

sLine = SourceFile.readline().rstrip()
saWords=sLine.split(",")
iNumCols=len(saWords)
iNumRows=iNumCols-4

print("There are "+repr(iNumCols)+" columns")

iaDay = [0 for i in range(iNumRows)]

for iDay in range(iNumRows):
    print(saWords[iDay+4])
    saDate=saWords[iDay+4].split("/")
    if int(saDate[0]) < 10:
        saDate[0] = "0"+saDate[0]
    if int(saDate[1]) < 10:
        saDate[1] = "0"+saDate[1]
    iaDay[iDay] = int(saDate[2]+saDate[0]+saDate[1])
