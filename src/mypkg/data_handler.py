import typing as tp
import sqlite3 as sq
import datetime
from dateutil import parser

def get_daily_data() ->tp.List[tp.Tuple[str,int]]:

    today_date = datetime.date.today().strftime("%Y-%m-%d")
    with sq.connect("database/my-db.db") as conn:
        res = conn.execute(            
            f"""
            SELECT DISTINCT
                denominazione_regione,
                SUM(totale_casi) OVER(PARTITION BY denominazione_regione, data) as totali_casi
                FROM (SELECT * FROM PROVINCE_DATA WHERE data LIKE '{today_date}%')
                ORDER BY totali_casi DESC, denominazione_regione ASC
            """
        ).fetchall()
        return res


def get_data_from_date_to_today(date: str) ->tp.List[tp.Tuple[str,int]]:
    date_str = parser.parse(date, yearfirst=True).strftime("%Y-%m-%d")
    with sq.connect("database/my-db.db") as conn:
        res = conn.execute(            
            f"""
            SELECT DISTINCT
                denominazione_regione,
                SUM(totale_casi) OVER(PARTITION BY denominazione_regione) as totali_casi
                FROM (SELECT * FROM PROVINCE_DATA WHERE data >= '{date_str}')                
                ORDER BY totali_casi DESC, denominazione_regione ASC
            """
        ).fetchall()
        return res
