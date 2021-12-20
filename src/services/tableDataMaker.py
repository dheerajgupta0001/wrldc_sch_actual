from typing import List, Tuple, TypedDict
import datetime as dt
import os
import pandas as pd
from src.typeDefs.schActualDrawalSummary import ISchActualDrawalSummary

def schActualTabledata(tableDf):

    tableDf['TIME_STAMP'] = tableDf['TIME_STAMP'].dt.date
    maxResult = tableDf.groupby('TIME_STAMP').max()
    minResult = tableDf.groupby('TIME_STAMP').min()
    avgResult = tableDf.groupby('TIME_STAMP').mean()

    maxResult.rename(columns = {'Schedule_Drawal':'maxSch', 'Actual_Drawal':'maxAct', 'UI_Drawal':'maxUI'}, inplace = True)
    minResult.rename(columns = {'Schedule_Drawal':'minSch', 'Actual_Drawal':'minAct', 'UI_Drawal':'minUI'}, inplace = True)
    avgResult.rename(columns = {'Schedule_Drawal':'avgSch', 'Actual_Drawal':'avgAct', 'UI_Drawal':'avgUI'}, inplace = True)

    tempData = pd.merge(maxResult, minResult, on="TIME_STAMP")
    finalData = pd.merge(tempData, avgResult, on="TIME_STAMP")
    # finalData = finalData.round(1)
    # round off then convert to int
    finalData = finalData.round(0).astype(int)
    finalData.reset_index(inplace = True)
    schACtualDrawalList: List[ISchActualDrawalSummary] = []
    for i in finalData.index:
        schActual: ISchActualDrawalSummary = {
            'date': dt.datetime.strftime(finalData['TIME_STAMP'][i], "%Y-%m-%d"),
            'maxActual': finalData['maxAct'][i],
            'minActual': finalData['minAct'][i],
            'maxSchedule': finalData['maxSch'][i],
            'minSchedule': finalData['minSch'][i],
            'avgSch': finalData['avgSch'][i],
            'avgAct': finalData['avgAct'][i],
            'maxUI': finalData['maxUI'][i],
            'minUI': finalData['minUI'][i],
            'avgUI': finalData['avgUI'][i]
            # 'avgAct': int(round(finalData['DEVIATION'][i]))
        }
        schACtualDrawalList.append(schActual)

    return schACtualDrawalList