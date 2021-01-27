#from src.fetchers.dayPmuAvailabilitySummaryFetcher import fetchPmuAvailabilitySummaryForDate
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from typing import List
from src.repos.fetchSemDataForDate import fetchSemSummaryForDate
from src.repos.testFetchSemDataForDate import testFetchSemSummaryForDate
from src.repos.fetchScadaDataForDate import fetchScadaSummaryForDate


def fetchScadaSemRawData(appDbConStr: str, scadaSemFolderPath: str, startDate: dt.datetime, endDate: dt.datetime, stateName: str) -> bool:
    """fetches the pmu availability data from excel files 
    and pushes it to the raw data table
    Args:
        appDbConStr (str): application db connection string
        pmuFolderPath (str): folder path of scad vs sem availability data excel files
        startDate (dt.datetime): start date
        endDate (dt.datetime): end date
    Returns:
        [bool]: returns True if succeded
    """
    #isRawDataFetchSuccess = False

    reqStartDt = startDate.date()
    reqEndDt = endDate.date()

    if reqEndDt < reqStartDt:
        return False

    currDate = reqStartDt
    semData = []
    scadaData = []
    times = []
    data = pd.DataFrame()
    while currDate <= reqEndDt:
        # fetch sem data for the date
        # print("sem data processing")
        # dailySemData = fetchSemSummaryForDate(scadaSemFolderPath, currDate, stateName)
        dailySemData = testFetchSemSummaryForDate(scadaSemFolderPath, currDate, stateName)
        # print(len(semData))
        semData.extend(dailySemData)
        # print("sem data processing ended")
        # fetch scada data and convert min wise to block wise
        dailyScadaData, timeStamp = fetchScadaSummaryForDate(scadaSemFolderPath, currDate, stateName)
        times.extend(timeStamp)
        # print("date")
        # print(times)
        scadaData.extend(dailyScadaData)

        currDate += dt.timedelta(days=1)
    dateList = []
    for col in times:
        dateList.append(dt.datetime.strftime(col, '%Y-%m-%d %H:%M:%S'))
    # print(dateList)
    # print(len(semData))
    data['scadaData']= scadaData
    data['semData']= semData
    data['times']= dateList
    # getting Difference 
    meterDataSum = data['semData'].sum()
    errorDiffList = data['scadaData'] - data['semData']
    errorSum = errorDiffList.sum() 
    errorPerc = round((errorSum/meterDataSum)*100, 2)
    # print(errorPerc)
    # convert dataframe to list of dictionaries
    resRecords = data.to_dict(orient='list')
    # print(resRecords)

    return resRecords, errorPerc