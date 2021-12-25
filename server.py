import datetime
import json
import socket
import threading
import tkinter
from tkinter import *
from Baza import BazaPodataka

sqlAutomobilInsert="""INSERT INTO AUTOMOBILI(Naziv,Cena) VALUES(?,?)"""
sqlAutomobiliSelectOba="""SELECT id, naziv, cena FROM AUTOMOBILI WHERE id=? AND cena=?"""
sqlAutomobiliSelect="""SELECT id, naziv, cena FROM AUTOMOBILI WHERE id=? OR cena=?"""
sqlAutomobiliSelectCount="""SELECT COUNT(*) 
                            FROM AUTOMOBILI 
                            WHERE id=?"""
sqlAutomobiliUpdate="""UPDATE AUTOMOBILI
                        SET cena = ?
                        WHERE id=?"""
sqlAutomobiliDelete="""DELETE FROM AUTOMOBILI
                        WHERE id=?"""

def upisiUListbox(datumVreme, zahtev, odgovor):
    lstbMsg.insert(0, datumVreme.strftime("%H:%M:%S") + " -> " + zahtev + " : " + odgovor)

def prihvatiZahteve():
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.bind((host, port))
    s.listen()

    while True:
        conn, addr = s.accept()
        try:
            odgovor=""
            poruka = json.loads(conn.recv(1024).decode())
            opcija = poruka["opcija"]
            datumVreme = datetime.datetime.now()

            if opcija == "nova tabela":
                odgovor = BazaPodataka.inicijalizacija()
                conn.send(json.dumps({"odgovor": odgovor}).encode())
                upisiUListbox(datumVreme,"Kreiranje nove tabele", odgovor)
            elif opcija == "novi automobil":
                odgovor = BazaPodataka.executSqlUpdate(sqlAutomobilInsert, (poruka["naziv"], poruka["cena"]))
                conn.send(json.dumps({"odgovor": "Operacija unosa novog zapisa je: "+odgovor}).encode())
                upisiUListbox(datumVreme, "Kreiranje novog zapisa", "Operacija unosa novog zapisa je: "+odgovor)
            elif opcija == "pretraga":
                sqlPretr= sqlAutomobiliSelectOba if poruka["oba"] else sqlAutomobiliSelect
                odgovor = BazaPodataka.executSqlSelect("Automobili",sqlPretr,(poruka["id"],poruka["cena"]))
                if  type(odgovor) is str:
                    conn.send(json.dumps({"odgovor": odgovor, "uspesno": False}).encode())
                    upisiUListbox(datumVreme, "Pretraga zapisa", odgovor)
                elif type(odgovor) is list:
                    if len(odgovor)==0:
                        conn.send(json.dumps({"odgovor": "Nema podataka za dati/e parametar/re!", "uspesno": True, "lista":[]}).encode())
                        upisiUListbox(datumVreme, "Pretraga zapisa", "Nema podataka pretrage za dati/e parametar/re!")
                    else:
                        conn.send(json.dumps({"odgovor": "Ima "+str(len(odgovor))+(" podatak" if len(odgovor)==1 else " podataka")+" pretrage za dati/e parametar/re!", "uspesno": True, "lista":list(map(lambda x:x.to_json(), odgovor))}).encode())
                        upisiUListbox(datumVreme, "Pretraga zapisa", "Ima "+str(len(odgovor))+(" podatak" if len(odgovor)==1 else " podataka")+" pretrage za dati/e parametar/re!")
            elif opcija == "azuriranje":
                odgovor = BazaPodataka.executSqlSelectCount(sqlAutomobiliSelectCount, (poruka["id"],))
                if type(odgovor) is str:
                    conn.send(json.dumps({"odgovor": odgovor}).encode())
                    upisiUListbox(datumVreme, "Azuriranje zapisa", odgovor)
                elif type(odgovor) is tuple:
                    br=odgovor[0]
                    if br == 0:
                        conn.send(json.dumps({"odgovor": "Nema podataka za azuriranje za uneti id!"}).encode())
                        upisiUListbox(datumVreme, "Azuriranje zapisa", "Nema podataka za azuriranje za uneti id!")
                    else:
                        odgovor = BazaPodataka.executSqlUpdate(sqlAutomobiliUpdate,(poruka["cena"],poruka["id"]))
                        conn.send(json.dumps({"odgovor": "Operacija azuriranja je: "+odgovor}).encode())
                        upisiUListbox(datumVreme, "Azuriranje zapisa", "Operacija azuriranja je: "+odgovor)
            elif opcija == "brisanje":
                odgovor = BazaPodataka.executSqlSelectCount(sqlAutomobiliSelectCount, (poruka["id"],))
                if type(odgovor) is str:
                    conn.send(json.dumps({"odgovor": odgovor}).encode())
                    upisiUListbox(datumVreme, "Brisanje zapisa", odgovor)
                elif type(odgovor) is tuple:
                    br=odgovor[0]
                    if br == 0:
                        conn.send(json.dumps({"odgovor": "Nema podataka za brisanje za uneti id!"}).encode())
                        upisiUListbox(datumVreme, "Brisanje zapisa", "Nema podataka za brisanje za uneti id!")
                    else:
                        odgovor = BazaPodataka.executSqlUpdate(sqlAutomobiliDelete,(poruka["id"],))
                        conn.send(json.dumps({"odgovor": "Operacija brisanja je: "+odgovor}).encode())
                        upisiUListbox(datumVreme, "Brisanje zapisa", "Operacija brisanja je: "+odgovor)
        except Exception as exp:
            print("%s" % exp)

        conn.close()


root=Tk()
root.title('Server')
root.geometry('100x800+0+0')
root.configure(background="steelblue")

#Label(root,text="Prikaz poruke sa servera:", bg="steelblue", font=("Verdana","8")).pack(pady=5)
frmMsg = Frame(root,  bg="steelblue")
frmMsg.pack(pady=5,fill="both", expand=True)
frmMsg.pack_propagate(False)
scrollbarlstbMsgY = Scrollbar(frmMsg,orient="vertical")
scrollbarlstbMsgY.pack(side=RIGHT, fill=Y)
scrollbarlstbMsgX = Scrollbar(frmMsg,orient="horizontal")
scrollbarlstbMsgX.pack(side=TOP, fill=X)
lstbMsg=Listbox(frmMsg,yscrollcommand = scrollbarlstbMsgY.set,xscrollcommand = scrollbarlstbMsgX.set,font=("Verdana", "9"))
lstbMsg.pack(fill=BOTH,expand=1)
scrollbarlstbMsgY.config(command = lstbMsg.yview)
scrollbarlstbMsgX.config(command = lstbMsg.xview)

t=threading.Thread(target=prihvatiZahteve,args=())
t.daemon=True
t.start()

root.mainloop()