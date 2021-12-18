from typing import List, Tuple, TypedDict
import cx_Oracle
import datetime as dt
import os
import pandas as pd
import matplotlib.pyplot as plt
from src.config.appConfig import getConfig
from flask import Flask, request, jsonify, render_template
from src.graphDataFetcher.scadaApiFetcher import ScadaApiFetcher
from src.graphDataFetcher.scadaSchPoint import scadaSchPoint
from src.graphDataFetcher.scadaActualPoint import scadaActualPoint
from src.typeDefs.schActualDrawalSummary import ISchActualDrawalSummary
from src.services.tableDataMaker import schActualTabledata

# get application config
appConfig = getConfig()

tokenUrl = appConfig['tokenUrl']
apiBaseUrl = appConfig['apiBaseUrl']
clientId = appConfig['clientId']
clientSecret = appConfig['clientSecret']
# creating instances of classes
obj_scadaApiFetcher = ScadaApiFetcher(tokenUrl, apiBaseUrl, clientId, clientSecret)

def fetchschVsDrawalData(constituentName: str, startDate: dt.datetime, endDate: dt.datetime):
    # for schedule
    schPoint = scadaSchPoint(constituentName)
    # print("Sch data")
    schData= obj_scadaApiFetcher.fetchData(schPoint, startDate, endDate)
    schDataDf = pd.DataFrame(schData, columns=['TIME_STAMP', 'Schedule_Drawal'])
    # print(schDataDf)

    # for drawal
    # print("Drawal data")
    actualPoint = scadaActualPoint(constituentName)
    drawalData = obj_scadaApiFetcher.fetchData(actualPoint, startDate, endDate)
    drawalDataDf = pd.DataFrame(drawalData, columns=['TIME_STAMP', 'Actual_Drawal'])
    # print(drawalDataDf)

    dfData_gInd = pd.merge(schDataDf, drawalDataDf, on="TIME_STAMP")

    # table data starts
    tableDf = dfData_gInd
    tableDf = schActualTabledata(tableDf)
    # tsable data ends

    times = dfData_gInd['TIME_STAMP']
    dateList = []
    for col in times:
        dateList.append(dt.datetime.strftime(col, '%Y-%m-%d %H:%M:%S'))
    dfData_gInd['TIME_STAMP']= dateList
    resRecords = dfData_gInd.to_dict(orient='list')
    # print(resRecords)

    # max min act sch
    maxActual = round(dfData_gInd['Actual_Drawal'].max())
    minActual = round(dfData_gInd['Actual_Drawal'].min())
    maxSchedule = round(dfData_gInd['Schedule_Drawal'].max())
    minSchedule = round(dfData_gInd['Schedule_Drawal'].min())
    #  end

    return resRecords, maxActual, minActual, maxSchedule, minSchedule