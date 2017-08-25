import requests as rq
import re

def html_tabela_kovancev ():
    raw_podatki = rq.get('https://coinmarketcap.com/all/views/all/').text
    regex_tabele = re.compile(
        r'<table class="table" id="currencies-all" style="font-size:14px">'
        r'(?P<tablebody>.*)'
        r'</table>',
        flags=re.DOTALL
    )
    return re.search(regex_tabele, raw_podatki).groupdict()['tablebody']

def html_kovanca (kovanec):
    request_url = 'https://coinmarketcap.com/currencies/'
    request_url += kovanec
    request_url += '/historical-data/?start=20170101&end=20171231'
    return rq.get(request_url).text

def podatki_vrstice (vrstica_html):
    regex_datuma = re.compile(r'<td class="text-left">(.*?)</td>', flags=re.DOTALL)
    datum = re.search(regex_datuma, vrstica_html).group(1)
    regex_podatkov = re.compile(r'<td>(.*?)</td>', flags=re.DOTALL)
    podatki = re.search(regex_podatkov, vrstica_html)
    vrstica = {'datum': datum}
    imena_podatkov = [
        'zacetna',
        'najnizja',
        'najvisja',
        'koncna',
        'volumen',
        'kapital'
    ]
    count = 0
    for podatek in re.finditer(regex_podatkov, vrstica_html):
        vrstica[imena_podatkov[count]] = float(podatek.group(1).replace(',', '').replace('-', '0'))
        count += 1
    return vrstica


def info_kovanca (kovanec):
    raw_kovanec = html_kovanca(kovanec)
    regex_vrstice = re.compile(
        r'<tr class="text-right">(.*?)</tr>',
        flags=re.DOTALL
    )
    podatki = []
    for vrstica in re.finditer(regex_vrstice, raw_kovanec):
        raw_vrstica = vrstica.group(1)
        podatki.append(podatki_vrstice(raw_vrstica))
    return podatki

def seznam_kovancev ():
    telo_tabele = html_tabela_kovancev()
    regex_coina = re.compile(r'<tr id="id-(\w*)"', flags=re.DOTALL)
    kovanci = []
    for kovanec in re.finditer(regex_coina, telo_tabele):
        kovanci.append(kovanec.group(1))
    return kovanci


