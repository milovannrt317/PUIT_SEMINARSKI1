# PUIT_SEMINARSKI1

Klijentska strana je Tkinter prozor veličine 800x800 piksela:
	1. Header klijenta, veličine 800x50, ima jednu funkcionalnost
koju obavlja nit (thread) u beskonačnoj petlji:
		- kreiranje i uklanjanje polukruga od kružnih isečaka
	2. Body klijenta, veličine 800x700, ima sledeće funkcionalnosti
koje se odnose na komunikaciju sa serverskom stranom:
		- programsko dugme za kreiranje nove prazne tabele
automobili čiji su atributi: id, naziv, cena i koja pripada
bazi baza01.db na serverskoj strani
		- unos novog zapisa automobila preko servera u datu bazu
		- čitanje zapisa automobila preko servera iz date baze
prema atributima:
			o id
			o cena
		- ažuriranje zapisa datog id u smislu promene vrednosti
atributa:
			o cena
		- brisanje zapisa prema filteru:
			o id
		- u listu se smeštaju odgovori servera.
	3. Footer klijenta, veličine 800x50, klijenta ima ispisano:
© 2021 Ime Prezime broj indeksa za članove tima


Serverska strana je Tkinter prozor veličine 100x800
	1. Serverska strana je povezana sa klijentskom stranom
korišćenjem TCP/IP komunikacije. Server komunicira sa
bazom podataka baza01.db prema zahtevima klijenta i vraća
odgovor klijentu. U listi se prikazuju zahtevi klijenta i
odgovori servera.
