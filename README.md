# Romani v knjigarni Felix 

Analizirala sem 1000 romanov (prvih 20 strani) [knjigarne Felix](http://felix.si/50-romani?n=54&id_category=50).

## Zajem podatkov 

Datoteka [romani.csv](csv_podatki/romani.csv) 
(v mapi csv_podatki) vsebuje vse zgoraj navedene podatke v istem vrstnem redu.
Najprej sem zajela prvih 50 strani, a ker je bilo zajetih premalo podatkov za posamezno knjigo, sem v htlm-jih teh
strani poiskala linke do strani s podatki posameznega romana. Koda je v datoteki 
[skripta.py](skripta.py).

Za vsako knjigo sem zajela:
* šifro
* naslov in avtorja
* ceno
* število strani in dimenzije
* leto izdaje
* ime prevajalca
* vezavo in založbo

## Analiza podatkov 

Delovne hipoteze:
* Katerega leta je izšlo največ romanov, ki jih hrani Felix?
* Kakšne so povezave med vezavo, ceno in številom strani romana?
* Kateri avtorji so napisali največ romanov in kateri prevajalci so jih največ prevedli?

Celotna analiza in rezultati so opisani v datoteki 
[Analiza_romanov.ipynb](Analiza_romanov.ipynb).

## Komantar 

Ljudem, ki si želijo analizirati podatke s strani knjigarne Felix, priporočam, da tega ne 
storijo, saj je spletna stran zelo nekonsistentna in je potrebno veliko ročne obdelave podatkov.