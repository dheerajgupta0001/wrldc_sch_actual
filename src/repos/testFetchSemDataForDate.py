import datetime as dt
#from src.typeDefs.pmuAvailabilitySummary import IPmuAvailabilitySummary
from typing import List
import os
import pandas as pd


def testFetchSemSummaryForDate(scadaSemFolderPath: str, targetDt: dt.datetime, stateName: str) -> List :
    """fetched pmu availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[]: list of sem data records fetched from the excel data
    """
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d%m%y')
    targetFilename = '{0}.{1}'.format(fileDateStr, stateName)
    targetFilePath = os.path.join(scadaSemFolderPath, targetFilename)
    print(targetFilePath)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        print("Excel file for date {0} is not present".format(targetDt))
        return []

    # read notepad type file format r"C:\Users\DEVANSH SHARMA\Desktop\example.txt",'r'
    with open(targetFilePath, mode='r') as f:
        # read all the file content   
        fLines = f.read()
        fLines = fLines.replace('\x00','').replace('\n\n', '\n').split('\n')
        # read header from first line
        # dfCols = fLines[7].split(',')[2:-1]
        schDfRows = []
        # read the values from line 1 to 100
        for rowInd in range(9,15):
            # read the data line
            dataRowVals = fLines[rowInd].split()
            dataRowVals = [k for k in dataRowVals[0:]]
            # print("row")
            # print(dataRowVals)
            schDfRows.append(dataRowVals)
        schDf = pd.DataFrame(data=schDfRows)
        # print(schDf)
    print(schDf)





    excelDf = pd.read_excel(targetFilePath, skiprows=9, skipfooter=3, header=None)
    if stateName == "DN1":
        excelDf = excelDf.iloc[:, [0,21]]
        excelDf.rename(columns = {0: 'Timestamp', 21:'semData'}, inplace = True)
    elif stateName == "DD1":
        excelDf = excelDf.iloc[:, [0,11]]
        excelDf.rename(columns = {0: 'Timestamp', 11:'semData'}, inplace = True)
    elif stateName == "GO1":
        excelDf = excelDf.iloc[:, [0,8]]
        excelDf.rename(columns = {0: 'Timestamp', 8:'semData'}, inplace = True)
    elif stateName == "CS1":
        excelDf = excelDf.iloc[:, [0,32]]
        excelDf.rename(columns = {0: 'Timestamp', 32:'semData'}, inplace = True)
    elif stateName == "MP2":
        excelDf = excelDf.iloc[:, [0,29]]
        excelDf.rename(columns = {0: 'Timestamp', 29:'semData'}, inplace = True)
    elif stateName == "MH2":
        excelDf = pd.read_excel(targetFilePath, skiprows=8, skipfooter=3, header=None)
        excelDf = excelDf.iloc[:, [0,30]]
        excelDf.rename(columns = {0: 'Timestamp', 30:'semData'}, inplace = True)
    elif stateName == "GU2":
        excelDf = excelDf.iloc[:, [0,32]]
        excelDf.rename(columns = {0: 'Timestamp', 32:'semData'}, inplace = True)
    # print("sem data")
    semData = excelDf["semData"].tolist()
    # print(excelDf)
    return semData