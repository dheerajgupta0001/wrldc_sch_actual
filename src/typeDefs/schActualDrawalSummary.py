from typing import TypedDict
import datetime as dt


class ISchActualDrawalSummary(TypedDict):
    date: dt.datetime
    maxActual: float
    minActual: float
    maxSchedule: float
    minSchedule: float
    avgSch: float
    avgAct: float
    maxUI: float
    minUI: float
    avgUI: float