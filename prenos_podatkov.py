import os
import csv
import orodja

def zagotovi_mapo ():
    if not os.path.exists('./podatki'):
        os.makedirs('./podatki')

def uvozi_podatke ():
    kovanci = orodja.seznam_kovancev()
    zagotovi_mapo()
    for kovanec in kovanci:
        print('Obdelava kovanca: ' + kovanec)
        podatki_kovanca = orodja.info_kovanca(kovanec) 
        print('Koncano branje, zacetek pisanja')
        with open('./podatki/' + kovanec + '.csv', 'w') as csv_datoteka:
            imena_stolpcev = [
                'datum',
                'zacetna',
                'najnizja',
                'najvisja',
                'koncna',
                'volumen',
                'kapital'
            ]
            pisanje = csv.DictWriter(csv_datoteka, fieldnames=imena_stolpcev)
            pisanje.writeheader()
            for podatek in reversed(podatki_kovanca):
                pisanje.writerow(podatek)
        print('Podatki o kovancu zapisani!\n')
