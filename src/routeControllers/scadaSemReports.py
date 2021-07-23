import calendar
from flask import Blueprint, render_template, request
import datetime as dt
import pandas as pd
from src.config.appConfig import getConfig
from src.graphDataFetcher.graphPlotDataFetcher import PlotScadaSemData
from src.graphDataFetcher.stateName import stateNameData
from src.reports.weekly.reportsReTable import fetchReErrorReportData
from src.reports.weekly.reportsIsgsTable import fetchIsgsErrorReportData
from src.reports.weekly.reportsConsTable import fetchConsErrorReportData


# get application config
appConfig = getConfig()
appDbConnStr = appConfig['appDbConStr']

scadaSemReportsPage = Blueprint('scadaSemReports', __name__,
                                template_folder='templates')
# get the instance of min_wise demand storage repository
# scadaSemReportsRepo= ScadaSemReportsSummaryRepo(appDbConnStr)


@scadaSemReportsPage.route('/weekly', methods=['GET', 'POST'])
# @role_required('code_book_editor')
def weekly():
    # in case of post request, fetch
    if request.method == 'POST':
        endDate = request.form.get('endDate')
        reportList = ["constituents", "re", "isgs"]
        for reportType in reportList:
            if reportType == "constituents":
                constituentsTableError, columnNameList = fetchConsErrorReportData(
                    endDate, appDbConnStr)
                print(reportType)

            elif reportType == "re":
                reTableError, reColumnNameList = fetchReErrorReportData(
                    endDate, appDbConnStr)
                print(reportType)
            elif reportType == "isgs":
                isgsTableError, isgsColumnNameList = fetchIsgsErrorReportData(
                    endDate, appDbConnStr)
                print(reportType)

        # testing of multiple div dynamically

        return render_template('scadaSemReport/weekly.html.j2',
                               constituentsTableError=constituentsTableError, columnNameList=columnNameList,
                               reTableError = reTableError, reColumnNameList = reColumnNameList,
                               isgsTableError = isgsTableError, isgsColumnNameList = isgsColumnNameList)
    # in case of get request just return the html template
    return render_template('scadaSemReport/weekly.html.j2')


@scadaSemReportsPage.route('/monthly', methods=['GET', 'POST'])
# @role_required('code_book_editor')
def monthly():
    # in case of post request, fetch
    if request.method == 'POST':
        endYear = int(request.form.get('year'))
        endMonth = int(request.form.get('month'))
        monthEndDay = calendar.monthrange(endYear, endMonth)[1]
        endMonthDate = dt.date(endYear, endMonth, monthEndDay)
        print(endMonthDate)
        # endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        # reportList = request.form.getlist('reList')
        # print(reportList)
        reportList = ["constituents", "re"]
        for reportType in reportList:
            print(reportType)

        # testing of multiple div dynamically

        return render_template('scadaSemReport/monthly.html.j2')
    # in case of get request just return the html template
    return render_template('scadaSemReport/monthly.html.j2')
