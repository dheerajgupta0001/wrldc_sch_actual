import datetime as dt
import pandas as pd
from src.graphDataFetcher.isgsDataFetcher.isgsName import isgsDisplayNameData
from src.graphDataFetcher.isgsDataFetcher.graphPlotDataFetcher import PlotScadaSemIsgsData


# get application config
def fetchIsgsErrorReportData(endDate, appDbConnStr: str):
    endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
    startDate = endDate - dt.timedelta(days=6)
    endDate1 = endDate - dt.timedelta(days=7)
    startDate1 = endDate1 - dt.timedelta(days=6)
    endDate2 = endDate - dt.timedelta(days=14)
    startDate2 = endDate2 - dt.timedelta(days=6)
    endDate3 = endDate - dt.timedelta(days=21)
    startDate3 = endDate3 - dt.timedelta(days=6)
    isgsList = ["AC-91", "BL-91", "CG-91", "DB-91", "DC-91", "DG-91", "DW-91", "EM-91", "GA-91",
                "GM-91", "JD-96", "JD-97", "JH-91", "JY-91", "KA-91", "KB-91", "KO-97", "KO-98",
                "KS-91", "KW-91", "LK-91", "MB-91", "MD-96", "MD-97", "MN-91", "NS-91", "RG-91",
                "RK-91", "SA-91", "SK-91", "SS-91", "TA-91", "TA-94", "TR-91", "VI-96",
                "VI-97", "VI-99", "VI-V4", "VI-V5", "SO-91", "LA-91", "GD-91", "KH-91"]
    # print(isgsList)
    # testing of multiple div dynamically
    dfData_g = []
    errorPerc1 = []
    errorPerc2 = []
    errorPerc3 = []
    errorPerc4 = []
    stateList = []
    isgsColumnNameList = []
    isgsColumnNameList.append("RE")
    for currIsgsName in isgsList:
        # get the instance of scada sem repository for GRAPH PLOTTING
        PlotScadaSemIsgsDataRepo = PlotScadaSemIsgsData(appDbConnStr)

        # fetch scada sem data from db via the repository instance of ith state
        dfData_gInd, errorPercWeek4 = PlotScadaSemIsgsDataRepo.plotScadaSemIsgsData(
            startDate3, endDate3, currIsgsName)

        dfData_gInd, errorPercWeek3 = PlotScadaSemIsgsDataRepo.plotScadaSemIsgsData(
            startDate2, endDate2, currIsgsName)

        dfData_gInd, errorPercWeek2 = PlotScadaSemIsgsDataRepo.plotScadaSemIsgsData(
            startDate1, endDate1, currIsgsName)

        dfData_gInd, errorPercWeek1 = PlotScadaSemIsgsDataRepo.plotScadaSemIsgsData(
            startDate, endDate, currIsgsName)

        state = isgsDisplayNameData(currIsgsName)
        stateList.append(state)
        dfData_g.append(dfData_gInd)
        errorPerc1.append(errorPercWeek1)
        errorPerc2.append(errorPercWeek2)
        errorPerc3.append(errorPercWeek3)
        errorPerc4.append(errorPercWeek4)
    endDate = dt.datetime.strftime(endDate, '%d-%m-%Y')
    endDate1 = dt.datetime.strftime(endDate1, '%d-%m-%Y')
    endDate2 = dt.datetime.strftime(endDate2, '%d-%m-%Y')
    endDate3 = dt.datetime.strftime(endDate3, '%d-%m-%Y')
    startDate = dt.datetime.strftime(startDate, '%d-%m-%Y')
    startDate1 = dt.datetime.strftime(startDate1, '%d-%m-%Y')
    startDate2 = dt.datetime.strftime(startDate2, '%d-%m-%Y')
    startDate3 = dt.datetime.strftime(startDate3, '%d-%m-%Y')
    week4 = str(startDate3) + " " + str(endDate3)
    week3 = str(startDate2) + " " + str(endDate2)
    week2 = str(startDate1) + " " + str(endDate1)
    week1 = str(startDate) + " " + str(endDate)
    isgsColumnNameList.append(week4)
    isgsColumnNameList.append(week3)
    isgsColumnNameList.append(week2)
    isgsColumnNameList.append(week1)

    isgsTableError = pd.DataFrame(
        {'isgs': stateList,
            'week1': errorPerc4,
            'week2': errorPerc3,
            'week3': errorPerc2,
            'week4': errorPerc1
            })
    isgsTableError = isgsTableError.to_records(index=False)
    isgsTableError = list(isgsTableError)

    return isgsTableError, isgsColumnNameList
