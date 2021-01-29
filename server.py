'''
This is the web server that acts as a service that creates outages raw data
'''
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup
from flask import Flask, request, jsonify, render_template
import datetime as dt
import pandas as pd
import json
import os
from waitress import serve
from src.config.appConfig import getConfig
from src.scadaSemDataFetcher.daywiseScadaSemDataFetcher import fetchScadaSemRawData
from src.repos.insertScadaSemToDb import ScadaSemSummaryRepo

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

# create pmu availability raw data between start and end dates
scadaSemFolderPath = appConfig['scadaSemFolderPath']
appDbConnStr = appConfig['appDbConStr']

# get the instance of min_wise demand storage repository
scadaSemRepo= ScadaSemSummaryRepo(appDbConnStr)

@app.route('/')
def hello():
    return render_template('home.html.j2')


@app.route('/createScadaSemData', methods=['GET', 'POST'])
def createScadaSemData():
    # in case of post request, fetch 
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        # print("tsting {}".format(startDate))
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        constituentsName = request.form.getlist('consList')
        # print(constituentsName)

        # testing of multiple div dynamically
        for stateName in constituentsName:
            isRawCreationSuccess= False
            #get the scada sem data of 1st state name for GRAPH PLOTTING
            dfData_gInd, errorPercInd, scadaSemRecord = fetchScadaSemRawData(appDbConnStr, scadaSemFolderPath,
                                                        startDate, endDate, stateName)
            isRawCreationSuccess = scadaSemRepo.pushScadaSemRecord(scadaSemRecord)
            if isRawCreationSuccess:
                print("Scada Sem data insertion SUCCESSFUL for {}".format(stateName))
            else:
                print("Scada Sem data insertion UNSUCCESSFUL for {}".format(stateName))
        # print(errorPerc[0])
        startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
        if isRawCreationSuccess:
            x=  {'message': 'Scada Sem Data insertion successful!!!'}
            return render_template('createScadaSemData.html.j2', data= x, startDate= startDate, endDate= endDate)

        return render_template('createScadaSemData.html.j2', startDate= startDate, endDate= endDate)
    # in case of get request just return the html template
    return render_template('createScadaSemData.html.j2')


@app.route('/plotGraphData', methods=['GET', 'POST'])
def plotGraphPmuData():
    # in case of post request, fetch 
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        print("tsting {}".format(startDate))
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        constituentsName = request.form.getlist('consList')
        print(constituentsName)

        # testing of multiple div dynamically
        dfData_g = []
        errorPerc = []
        for stateName in constituentsName:
            isFetchSuccess= False
            #get the scada sem data of 1st state name for GRAPH PLOTTING
            dfData_gInd, errorPercInd, scadaSemRecord = fetchScadaSemRawData(appDbConnStr, scadaSemFolderPath,
                                                        startDate, endDate, stateName)
            isFetchSuccess = scadaSemRepo.pushScadaSemRecord(scadaSemRecord)
            if isFetchSuccess:
                print("Scada Sem data insertion SUCCESSFUL for {}".format(stateName))
            else:
                print("Scada Sem data insertion UNSUCCESSFUL for {}".format(stateName))
            dfData_g.append(dfData_gInd)
            errorPerc.append(errorPercInd)
        # print(errorPerc[0])
        startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
        div_info = zip(constituentsName, errorPerc)
        # print(errorPerc)

        return render_template('test.html.j2', data= dfData_g, div_info= div_info, consName= constituentsName,
                                    stateName= stateName, startDate= startDate, endDate= endDate)
    # in case of get request just return the html template
    return render_template('test.html.j2')


if __name__ == '__main__':
    app.run(port=int(appConfig['flaskPort']), debug=True)
    serverMode: str = appConfig['mode']
    if serverMode.lower() == 'd':
        app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(appConfig['flaskPort']), threads=1)
