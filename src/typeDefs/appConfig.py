from typing import TypedDict
import datetime as dt


class IAppConfig(TypedDict):
    appDbConStr: str
    tokenUrl: str
    apiBaseUrl: str
    clientId: str
    clientSecret: str