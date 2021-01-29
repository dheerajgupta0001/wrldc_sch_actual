from typing import TypedDict
import datetime as dt


class IScadaSemSummary(TypedDict):
    time_stamp: dt.datetime
    SCADA_DATA: float
    SEM_DATA: float
    CONSTITUENTS_NAME: str
