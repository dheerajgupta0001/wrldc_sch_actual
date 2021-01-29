import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.scadaSemSummary import IScadaSemSummary

class ScadaSemSummaryRepo():
    """Repository class for day Wise Max Demand data
    """
    """This class pushes Scada-Sem data To "scada_warehouse.SCADA_SEM" table
    """
    connString: str = ""
    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """

        self.connString = con_string

    def pushScadaSemRecord(self, scadaSemRecords: List[IScadaSemSummary]) -> bool:
        """inserts Scada-Sem data To "scada_warehouse.SCADA_SEM" table
        Args:
            scadaSemRecords (List[IScadaSemSummary]): scada Sem Records to be inserted
        Returns:
            bool: returns true if process is ok
        """
        # get connection with raw data table
        connection= cx_Oracle.connect(self.connString)
        isInsertSuccess = True
        if len(scadaSemRecords) == 0:
            return isInsertSuccess
        try:
            # keyNames names of the raw data
            keyNames = ['time_stamp', 'SCADA_DATA', 'SEM_DATA', 'CONSTITUENTS_NAME']
            colNames = ['TIME_STAMP', 'SCADA_DATA', 'SEM_DATA', 'CONSTITUENTS_NAME']
            # get cursor for raw data table
            cursor=connection.cursor()

            # text for sql place holders
            sqlPlceHldrsTxt = ','.join([':{0}'.format(x+1)
                                        for x in range(len(keyNames))])

            # delete the rows which are already present
            existingScadaSemData = [(x['time_stamp'], x['CONSTITUENTS_NAME'] )
                                  for x in scadaSemRecords]
            # print("deletion started")
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
            cursor.executemany(
                "delete from mis_warehouse.SCADA_SEM where TIME_STAMP=:1 and CONSTITUENTS_NAME=:2", existingScadaSemData)
            # print("deletion is done")
            
            # insert the raw data
            sql_insert = "insert into mis_warehouse.SCADA_SEM({0}) values ({1})".format(
                ','.join(colNames), sqlPlceHldrsTxt)
            
            # cursor.execute("ALTER USER <scada_warehouse> quota unlimited on <scada_sem>;")
            # cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
            cursor.executemany(sql_insert, [tuple(
                [r[col] for col in keyNames]) for r in scadaSemRecords])
            # commit the changes
            connection.commit()
        except Exception as e:
            isInsertSuccess = False
            print('Error while bulk insertion of Scada Sem data into database')
            print(e)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            
        return isInsertSuccess
