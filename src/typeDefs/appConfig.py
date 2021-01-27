from typing import TypedDict
import datetime as dt


class IAppConfig(TypedDict):
    appDbConStr: str
    csadaSemFolderPath: str
