"""

Plot COVID-19 data in 2D.

Author: Rory Barnes
Date: 4 May 2020

"""

import numpy as np
import string as str
import subprocess as subp
import csv
import subprocess as subp
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sys
#try:
#    import vplot as vpl
#except:
#    print('Cannot import vplot. Please install from https://github.com/VirtualPlanetaryLaboratory/vplot.')

# Check correct number of arguments
if (len(sys.argv) != 2):
    print('ERROR: Incorrect number of arguments.')
    print('Usage: python '+sys.argv[0]+' <pdf | png>')
    exit(1)
if (sys.argv[1] != 'pdf' and sys.argv[1] != 'png'):
    print('ERROR: Unknown file format: '+sys.argv[1])
    print('Options are: pdf, png')
    exit(1)

sSource="covid19-global-3May2020.csv"
csvData = csv.reader(open(sSource,"r"))
saHeader = next(csvData)

iLines = 2576
iaCountryID = [0 for j in range(iLines)]
iaDays = [0 for j in range(iLines)]
iaCumCases = [0 for j in range(iLines)]
iaNewCases = [0 for j in range(iLines)]
iaCumDeaths = [0 for j in range(iLines)]
iaNewDeaths = [0 for j in range(iLines)]
daDeathsPerMil = [0. for j in range(iLines)]
daCasesPerMil = [0. for j in range(iLines)]
iaPop = [0 for j in range(iLines)]
saCountry = ["" for j in range(iLines)]
saDate = ["" for j in range(iLines)]

iLine = 0
for saLine in csvData:
    iaCountryID[iLine] = int(saLine[1])
    iaDays[iLine] = int(saLine[2])
    iaCumCases[iLine] = int(saLine[3])
    iaNewCases[iLine] = int(saLine[4])
    daCasesPerMil[iLine] = float(saLine[5])
    iaCumDeaths[iLine] = int(saLine[6])
    iaNewDeaths[iLine] = int(saLine[7])/100
    daDeathsPerMil[iLine] = float(saLine[8])
    iaPop[iLine] = int(saLine[9])/1e7
    saCountry[iLine] = saLine[10]
    saDate[iLine] = saLine[11]
    #print(repr())
    iLine += 1

fig = plt.figure(figsize=(5,4))
plt.scatter(iaDays,iaCumDeaths,s=iaNewDeaths,c=iaCountryID,cmap=plt.cm.tab20)
plt.xlabel('Days Since 22 Jan 2020',fontsize=18)
plt.ylabel('Cumulative Deaths',fontsize=18)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

#vpl.make_pretty(fig)
if (sys.argv[1] == 'pdf'):
    plt.savefig('covid2D.pdf', bbox_inches="tight", dpi=600)
if (sys.argv[1] == 'png'):
    plt.savefig('covid2D.png', bbox_inches="tight", dpi=600)
plt.close()
