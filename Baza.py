import sqlite3
from tkinter import messagebox
from Automobil import Automobil


class BazaPodataka():
    conn=None
    cursor=None
    database = 'baza01.db'

    @staticmethod
    def connect():
        BazaPodataka.conn = sqlite3.connect(BazaPodataka.database)
        BazaPodataka.cursor = BazaPodataka.conn.cursor()

    @staticmethod
    def disconnect():
        BazaPodataka.conn.close()

    @staticmethod
    def inicijalizacija():
        poruka=""
        try:
            BazaPodataka.connect()

            if BazaPodataka.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='AUTOMOBILI'").fetchone()[0] > 0:
                BazaPodataka.cursor.execute("DROP TABLE AUTOMOBILI")

            BazaPodataka.cursor.execute("""
                    CREATE TABLE AUTOMOBILI
                    ( Id INTEGER PRIMARY KEY AUTOINCREMENT,
                      Naziv NCHAR (20) NOT NULL,
                      Cena FLOAT (1) NOT NULL,
                      CONSTRAINT uk_grupa_naziv UNIQUE (Naziv)
                    )
                """)

            BazaPodataka.conn.commit()
            poruka = "Uspesno kreirana tabela AUTOMOBILI!"
        except Exception as exc:
            BazaPodataka.conn.rollback()
            poruka = "Problem sa bazom podataka!\n%s" % exc
        finally:
            BazaPodataka.disconnect()
        return poruka
    @staticmethod
    def executSqlSelect(klasa, sqlQuery,args=()):
        podaci=""
        try:
            BazaPodataka.connect()
            podaci2=BazaPodataka.cursor.execute(sqlQuery, args).fetchall()

            odg = []
            if klasa=="Automobili":
                for row in podaci2:
                    aut = Automobil(row[0], row[1], row[2])
                    odg.append(aut)
            podaci=odg.copy()
        except Exception as exc:
            podaci = "Problem sa bazom podataka!\n%s" % exc
        finally:
            BazaPodataka.disconnect()
        return podaci
    @staticmethod
    def executSqlUpdate(sqlQuery,args=()):
        poruka = ""
        try:
            BazaPodataka.connect()
            BazaPodataka.cursor.execute(sqlQuery,args)
            BazaPodataka.conn.commit()
            poruka = "Uspesno odradjena izmena nad bazom podataka!"
        except Exception as exc:
            poruka = "Neuspesno odradjena izmena nad bazom podataka\n%s" % exc
            BazaPodataka.conn.rollback()
        finally:
            BazaPodataka.disconnect()
        return poruka

    @staticmethod
    def executSqlSelectCount(sqlQuery, args=()):
        podaci = ""
        try:
            BazaPodataka.connect()
            podaci = BazaPodataka.cursor.execute(sqlQuery, args).fetchone()
        except Exception as exc:
            podaci = "Problem sa bazom podataka!\n%s" % exc
        finally:
            BazaPodataka.disconnect()
        return podaci