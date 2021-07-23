import datetime as dt
import pandas as pd
from src.graphDataFetcher.reDataFetcher.reName import reDisplayNameData
from src.graphDataFetcher.reDataFetcher.graphPlotDataFetcher import PlotScadaSemReData


# get application config
def fetchReErrorReportData(endDate, appDbConnStr: str):
    endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
    startDate = endDate - dt.timedelta(days=6)
    endDate1 = endDate - dt.timedelta(days=7)
    startDate1 = endDate1 - dt.timedelta(days=6)
    endDate2 = endDate - dt.timedelta(days=14)
    startDate2 = endDate2 - dt.timedelta(days=6)
    endDate3 = endDate - dt.timedelta(days=21)
    startDate3 = endDate3 - dt.timedelta(days=6)
    reList = ["OS-91", "AM-91", "MA-91", "AR-91", "RE-91",
              "GI-91", "GI-94", "IX-91", "AG-91", "AF-91", "GH-91"]
    # print(reList)
    # testing of multiple div dynamically
    dfData_g = []
    errorPerc1 = []
    errorPerc2 = []
    errorPerc3 = []
    errorPerc4 = []
    stateList = []
    reColumnNameList = []
    reColumnNameList.append("RE")
    for currReName in reList:
        # get the instance of scada sem repository for GRAPH PLOTTING
        plotScadaSemReDataRepo = PlotScadaSemReData(appDbConnStr)

        # fetch scada sem data from db via the repository instance of ith state
        dfData_gInd, errorPercWeek4 = plotScadaSemReDataRepo.plotScadaSemReData(
            startDate3, endDate3, currReName)

        dfData_gInd, errorPercWeek3 = plotScadaSemReDataRepo.plotScadaSemReData(
            startDate2, endDate2, currReName)

        dfData_gInd, errorPercWeek2 = plotScadaSemReDataRepo.plotScadaSemReData(
            startDate1, endDate1, currReName)

        dfData_gInd, errorPercWeek1 = plotScadaSemReDataRepo.plotScadaSemReData(
            startDate, endDate, currReName)

        state = reDisplayNameData(currReName)
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
    reColumnNameList.append(week4)
    reColumnNameList.append(week3)
    reColumnNameList.append(week2)
    reColumnNameList.append(week1)

    reTableError = pd.DataFrame(
        {'re': stateList,
            'week1': errorPerc4,
            'week2': errorPerc3,
            'week3': errorPerc2,
            'week4': errorPerc1
            })
    reTableError = reTableError.to_records(index=False)
    reTableError = list(reTableError)

    return reTableError, reColumnNameList
