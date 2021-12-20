'''
This is the web server that acts as a service that creates scada sem data
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
from src.graphDataFetcher.stateName import stateNameData
from src.graphDataFetcher.scadaApiFetcher import ScadaApiFetcher
from src.repos.schVsDrawalDataFetcher import fetchschVsDrawalData
from src.services.tableDivName import tableDivNameRet

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

@app.route('/')
def hello():
    return render_template('home.html.j2')


@app.route('/plotGraph', methods=['GET', 'POST'])
def plotGraph():
    # in case of post request, fetch 
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        # print("tsting {}".format(startDate))
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        constituentName = request.form.getlist('stateName')
        # constituentName = request.form.get('stateName')
        # print(constituentName)

        # multiple div dynamically
        # maxActual = []
        # minActual = []
        # maxSchedule = []
        # minSchedule = []
        dfData_g = []
        stateList = []
        divItrs = []
        tableDiv = []
        tableDf_g = []
        for cItr, stateName in enumerate(constituentName):
            # print(stateName)
            dfData_gInd, tableDf = fetchschVsDrawalData(stateName, startDate, endDate)
            # print(dfData_gInd)
            # print(tableDf)
            state= stateNameData(stateName)
            stateList.append(state)
            tableDiv.append(tableDivNameRet(stateName))
            dfData_g.append(dfData_gInd)
            divItrs.append(cItr+1)
            tableDf_g.append(tableDf)

        startDate = dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strftime(endDate, '%Y-%m-%d')
        div_info = zip(constituentName, divItrs, tableDiv, tableDf_g)

        return render_template('plotTest.html.j2', data= dfData_g, div_info= div_info,
                                consName= constituentName, stateList= stateList,
                                startDate= startDate, endDate= endDate,
                                tableDiv= tableDiv)


        return render_template('plotTest.html.j2')
    # in case of get request just return the html template
    return render_template('plotTest.html.j2')


if __name__ == '__main__':
    serverMode: str = appConfig['mode']
    if serverMode.lower() == 'p':
        app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(appConfig['flaskPort']), threads=1)
