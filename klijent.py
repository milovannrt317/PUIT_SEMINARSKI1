import datetime
import threading
import time
import tkinter
from tkinter import *
from tkinter import messagebox

from Automobil import Automobil
from Socket_klijent import KlijentSock

sock=KlijentSock()

#funkcije iskoriscene za ogranicavanje unosa korisnika na samo brojevne vrednosti
def tryFloatInt(st,opc):
    try:
        if opc=='int':
            int(st)
        else:
            float(st)
        return True
    except ValueError:
        return False

def validateFloat(P):
    if P == "" or tryFloatInt(P,"float"):
        return True
    else:
        return False

def validateInt(P):
    if P == "" or tryFloatInt(P,"int"):
        return True
    else:
        return False


def upisiOdgovor(odgovor):
    datumVreme = datetime.datetime.now()
    lstbMsg.insert(0, datumVreme.strftime("%H:%M:%S") + " -> " + odgovor)

def novaTabela():
    odgovor = sock.request({"opcija": "nova tabela"})
    upisiOdgovor(odgovor["odgovor"])

def noviZapis():
    if entNazivUns.get()=="" or entCenaUns.get()=="":
        messagebox.showerror("Greska!", "Neuphodno je uneti naziv i cenu automobila za kreiranje novog zapisa!")
        return
    odgovor = sock.request({"opcija": "novi automobil", "naziv": entNazivUns.get(), "cena": float(entCenaUns.get())})
    upisiOdgovor(odgovor["odgovor"])
    entNazivUns.delete(0,END)
    entCenaUns.delete(0,END)

def pretragaZapisa():
    idAut=entIDPretr.get()
    cenaAut=entCenaPretr.get()
    if idAut=="" and cenaAut=="":
        messagebox.showerror("Greska!", "Oba polja za pretragu su prazna!")
        return
    idAut=int(idAut) if idAut!="" else -100
    cenaAut=float(cenaAut) if cenaAut!="" else -100

    obaUneta=False
    if idAut!=-100 and cenaAut!=-100:
        obaUneta=True
    odgovor=sock.request({"opcija": "pretraga", "id": idAut, "cena": cenaAut, "oba":obaUneta})
    upisiOdgovor(odgovor["odgovor"])

    if odgovor["uspesno"]:
        listaAut=list(map(lambda x: Automobil.from_json(x), odgovor["lista"]))
        lstbAut.delete(0,END)
        for x in listaAut:
            lstbAut.insert(END,str(x))
    entIDPretr.delete(0, END)
    entCenaPretr.delete(0, END)

def azuriranjeZapisa():
    idAut = entIDAzr.get()
    cenaAut = entCenaAzr.get()
    if idAut == "" or cenaAut == "":
        messagebox.showerror("Greska!", "Moraju oba polja biti uneta da bi se izvrsilo azurianje zapisa!")
        return
    odgovor = sock.request({"opcija": "azuriranje", "id": int(idAut), "cena": float(cenaAut)})
    upisiOdgovor(odgovor["odgovor"])
    entIDAzr.delete(0, END)
    entCenaAzr.delete(0, END)

def brisanjeZapisa():
    idAut = entIDBrs.get()
    if idAut == "":
        messagebox.showerror("Greska!", "Mora biti unet id da bi se izvrsilo brisanje zapisa!")
        return
    odgovor = sock.request({"opcija": "brisanje", "id": int(idAut)})
    upisiOdgovor(odgovor["odgovor"])
    entIDBrs.delete(0, END)

boolkraj=True

def crtaj(pomeraj):
    global C, boolkraj
    coord = 350, 10, 450, 85
    pocetak=0
    while boolkraj:
        arc = C.create_arc(coord, start=0, extent=pocetak, fill="red")
        pocetak += pomeraj
        if pocetak==180 or pocetak==0:
            pomeraj=pomeraj*-1
        time.sleep(0.1)
        C.delete(arc)
    C.delete("all")



root=Tk()
root.title('Klijent')
root.geometry('800x800+{}+{}'.format((root.winfo_screenwidth() // 2) - (800 // 2),
                                         (root.winfo_screenheight() // 2) - (800 // 2)))  #za centriranje prozora na sredinu ekrana

vcmdF = (root.register(validateFloat))
vcmdI = (root.register(validateInt))

header=Frame(root, height=50, width=800)
header.pack()

C = tkinter.Canvas(header, bg="yellow", height=50, width=800)
C.pack()


body=Frame(root,bg="lightblue", height=700, width=800)
body.pack()
body.pack_propagate(False)  #da se ne skupi frame na velicinu elemenata koji su u njemu


btnNovaTbl=Button(body,text="Kreiraj novu praznu tabelu AUTOMOBILI", font=("Verdana","10"), command=novaTabela)
btnNovaTbl.pack(pady=(20,10))

#grupsainje dva frame radi ustede prostora
frmGrpUnsAzr=Frame(body, bg="lightblue", width=800)
frmGrpUnsAzr.pack(fill="both", expand=True,pady=10)

frmUns=Frame(frmGrpUnsAzr, bg="lightblue", width=300)
frmUns.pack(side = LEFT, fill="both", expand=True, padx=50)

Label(frmUns,text="Unos novog automobila:", bg="lightblue", font=("Verdana","10")).pack(pady=10)

Label(frmUns,text="Naziv automobila:", bg="lightblue", font=("Verdana","8")).pack(pady=(10,5))
entNazivUns=Entry(frmUns, font=("Verdana","9"))
entNazivUns.pack(pady=5)

Label(frmUns,text="Cena automobila:", bg="lightblue", font=("Verdana","8")).pack(pady=5)
entCenaUns=Entry(frmUns, font=("Verdana","9"), validate='all', validatecommand=(vcmdF, '%P'))
entCenaUns.pack(pady=5)

btnUnosAut=Button(frmUns,text="Unesi automobil", font=("Verdana","9"), command=noviZapis)
btnUnosAut.pack(pady=(5,10))


frmAzr=Frame(frmGrpUnsAzr, bg="lightblue", width=300)
frmAzr.pack(side = RIGHT, fill="both", expand=True, padx=50)

Label(frmAzr,text="Azuriranje automobila:", bg="lightblue", font=("Verdana","10")).pack(pady=10)

Label(frmAzr,text="Id automobila:", bg="lightblue", font=("Verdana","8")).pack(pady=(10,5))
entIDAzr=Entry(frmAzr, font=("Verdana","9"), validate='all', validatecommand=(vcmdI, '%P'))
entIDAzr.pack(pady=5)

Label(frmAzr,text="Cena automobila:", bg="lightblue", font=("Verdana","8")).pack(pady=5)
entCenaAzr=Entry(frmAzr, font=("Verdana","9"), validate='key', validatecommand=(vcmdF, '%P'))
entCenaAzr.pack(pady=5)

btnAzrAut=Button(frmAzr,text="Azuriraj automobil", font=("Verdana","9"), command=azuriranjeZapisa)
btnAzrAut.pack(pady=(5,10))


frmGrpPretr=Frame(body, bg="lightblue", width=800)
frmGrpPretr.pack(fill="both", expand=True,pady=10)

frmPretrAut=Frame(frmGrpPretr, bg="lightblue", width=300)
frmPretrAut.pack(side = LEFT, fill="both", expand=True, padx=50)

Label(frmPretrAut,text="Pretraga automobila:", bg="lightblue", font=("Verdana","9")).pack(pady=10)

Label(frmPretrAut,text="Id automobila:", bg="lightblue", font=("Verdana","8")).pack(pady=(10,5))
entIDPretr=Entry(frmPretrAut, font=("Verdana","9"), validate='all', validatecommand=(vcmdI, '%P'))
entIDPretr.pack(pady=5)

Label(frmPretrAut,text="Cena automobila:", bg="lightblue", font=("Verdana","8")).pack(pady=5)
entCenaPretr=Entry(frmPretrAut, font=("Verdana","9"), validate='key', validatecommand=(vcmdF, '%P'))
entCenaPretr.pack(pady=5)

btnPretrAut=Button(frmPretrAut,text="Pretrazi automobil/e", font=("Verdana","9"), command=pretragaZapisa)
btnPretrAut.pack(pady=(5,10))


frmPretrPrkz=Frame(frmGrpPretr, bg="lightblue", width=350)
frmPretrPrkz.pack(side = RIGHT, fill="both", expand=True, padx=(50,20))


Label(frmPretrPrkz,text="Prikaz pretrazenog/ih automobila:", bg="lightblue", font=("Verdana","9")).pack(pady=5)
frmPretrAutP=Frame(frmPretrPrkz, width=350)
frmPretrAutP.pack(pady=(5,10),fill="both", expand=True)
frmPretrAutP.pack_propagate(False)
scrollbarlstbAutY = Scrollbar(frmPretrAutP,orient="vertical")
scrollbarlstbAutY.pack(side=RIGHT, fill=Y)
scrollbarlstbAutX = Scrollbar(frmPretrAutP,orient="horizontal")
scrollbarlstbAutX.pack(side=BOTTOM, fill=X)
lstbAut=Listbox(frmPretrAutP,yscrollcommand = scrollbarlstbAutY.set,xscrollcommand = scrollbarlstbAutX.set,font=("Verdana", "9"))
lstbAut.pack(fill=BOTH,expand=1)
scrollbarlstbAutY.config(command = lstbAut.yview)
scrollbarlstbAutX.config(command = lstbAut.xview)


frmGrpBrsMsgSrv = Frame(body, bg="lightblue", width=800)
frmGrpBrsMsgSrv.pack(fill="both", expand=True, pady=10)

frmBrsAut = Frame(frmGrpBrsMsgSrv, bg="lightblue", width=300)
frmBrsAut.pack(side = LEFT, fill="both", expand=True, padx=50)

Label(frmBrsAut,text="Brisanje automobila:", bg="lightblue", font=("Verdana","9")).pack(pady=10)

Label(frmBrsAut,text="Id automobila:", bg="lightblue", font=("Verdana","8")).pack(pady=(10,5))
entIDBrs=Entry(frmBrsAut, font=("Verdana","9"), validate='all', validatecommand=(vcmdI, '%P'))
entIDBrs.pack(pady=5)

btnBrsAut = Button(frmBrsAut,text="Obrisi automobil/e", font=("Verdana","9"), command=brisanjeZapisa)
btnBrsAut.pack(pady=(5,10))


frmMsgPrkz = Frame(frmGrpBrsMsgSrv, bg="lightblue", width=350)
frmMsgPrkz.pack(side = RIGHT, fill="both", expand=True, padx=(50,20))


Label(frmMsgPrkz,text="Prikaz poruke sa servera:", bg="lightblue", font=("Verdana","9")).pack(pady=5)
frmMsg = Frame(frmMsgPrkz, width=350)
frmMsg.pack(pady=(5,10),fill="both", expand=True)
frmMsg.pack_propagate(False)
scrollbarlstbMsgY = Scrollbar(frmMsg,orient="vertical")
scrollbarlstbMsgY.pack(side=RIGHT, fill=Y)
scrollbarlstbMsgX = Scrollbar(frmMsg,orient="horizontal")
scrollbarlstbMsgX.pack(side=BOTTOM, fill=X)
lstbMsg=Listbox(frmMsg,yscrollcommand = scrollbarlstbMsgY.set,xscrollcommand = scrollbarlstbMsgX.set,font=("Verdana", "9"))
lstbMsg.pack(fill=BOTH,expand=1)
scrollbarlstbMsgY.config(command = lstbMsg.yview)
scrollbarlstbMsgX.config(command = lstbMsg.xview)


footer=Frame(root, height=50, width=800, bg="salmon")
footer.pack()
footer.pack_propagate(False)

Label(footer,text="© 2021 Nikola Jovicic RIN-47/20\nMilovan Lazic RIN-48/20", bg="salmon").pack()

t=threading.Thread(target=crtaj,args=(10,))
t.daemon=True
t.start()

root.mainloop()