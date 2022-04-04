import pandas as pd
import sqlite3 as sq

def setUp() -> None:

    with sq.connect("database/my-db.db") as conn:
    
        conn.executescript(
            """
                CREATE TABLE IF NOT EXISTS PROVINCE_DATA (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                data DATE,
                stato VARCHAR(50),
                codice_regione INTEGER,
                denominazione_regione VARCHAR(50),
                codice_provincia INTEGER,
                denominazione_provincia VARCHAR(50),
                sigla_provincia VARCHAR(50),
                lat NUMERIC,
                long NUMERIC,
                totale_casi INTEGER,
                note VARCHAR(50),
                codice_nuts_1 VARCHAR(50),
                codice_nuts_2 VARCHAR(50),
                codice_nuts_3 VARCHAR(50)
            ); 
            DELETE FROM PROVINCE_DATA;          
            """
        )
        data = pd.read_json(
            "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json",
            orient="records",
            convert_dates=["data"]
        )
        #_ = data[data['data']=='2022-04-03 17:00:00']
        #_ = data[data['denominazione_regione']=='Lombardia']
        #print(sum(_['totale_casi']))
        data.to_sql('PROVINCE_DATA', con=conn, if_exists='append', index=False)


