import requests
import re
import os
import csv

romani_url = 'http://felix.si/50-romani?n=54&id_category=50'
romani_directory = 'podatki'
romani_directory_new = 'novi_podatki'
page_filename = 'page'  #.html
page_filename_new = 'new_page'  #.html
csv_directory = 'csv_podatki'
csv_filename = 'romani.csv'

empty_key = '-'
keys = ['sifra', 'naslov', 'avtor', 'cena_v_evrih', 'stevilo_strani', 'dimenzije', 'leto_izdaje', 'prevajalec', 'vezava', 'zalozba']


#s strni z url-jem url pobere html
def download_url_to_string(url):
    try:
        url_get = requests.get(url)
    except:
        return "Tole pa ni šlo."
    return url_get.text


#v mapi directory naredi file filename z vsebino text
def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


#pobere in shrani html-je z vseh dvajsetih strani
def save_strings_to_files():
    for i in range(1, 21):
        if i == 1:
            save_string_to_file(download_url_to_string(romani_url), romani_directory, page_filename + '{}'.format(i) + '.html')
        else:
            save_string_to_file(download_url_to_string(romani_url + '&p={}'.format(i)), romani_directory, page_filename + '{}'.format(i) + '.html')
    return None


#snete prve strani
##############################################################################################################


#prebere stran v filename-u v mapi directory
def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


#iz html-ja strani poišče linke, ki vodijo do romanov
def find_links(directory, filename):
    text = read_file_to_string(directory, filename)
    rx = re.compile(r'href="http://felix\.si/*?/[^"]*?\.html"')
    links = re.findall(rx, text)
    links = set(links)
    linki_romanov = set()
    for l in links:
        if ('romani' in l) or ('kriminalk' in l):
            linki_romanov.add(l[6:-1])
    return linki_romanov


#skombinira html-je z linkov neke strani
def save_links_to_file(list_of_links, directory, filename):
    text = ''
    for i in list_of_links:
        text += download_url_to_string(i)
    save_string_to_file(text, directory, filename)


#shrani 20 skombiniranih html-jev 
def new_html_files():
    for i in range(1, 21):
        links = find_links(romani_directory, 'page{}.html'.format(i))
        save_links_to_file(links, romani_directory_new, page_filename_new + '{}.html'.format(i))


#snete notranje strani
##############################################################################################################
def spremen(niz):
    nizz = ''
    for znak in niz:
        if znak in '0123456789':
            nizz += znak
    return nizz

#razdeli nove html-je na posamezne knjige
def page_to_ads(page):
    rx = re.compile(r'<!DOCTYPE.*?</html>',
                    re.DOTALL)
    ads = re.findall(rx, page)
    return ads


#najde podatke enega romana
def make_a_dictionary(ad):
    dictionary = {}
    tab = keys
    rx_list = [r'<span >Šifra: </span> (?P<sifra>.*?)</li>',
               r'<title >(?P<naslov>.*?) - FELIX.si</title>',
               r'<span >Avtor: </span> (?P<avtor>.*?)</li>',
               r'<span id="our_price_display">(?P<cena_v_evrih>.*?)</span>',
               r'<span >&Scaron;tevilo strani: </span> (?P<stevilo_strani>.*?)</li>',
               r'<span >Dimenzije: </span> (?P<dimenzije>.*?)</li>',
               r'<span >Leto izdaje: </span> (?P<leto_izdaje>.*?)</li>',
               r'<span >Prevajalec: </span> (?P<prevajalec>.*?)</li>',
               r'<span >Vezava: </span> (?P<vezava>.*?)</li>',
               r'<span >Založba: </span> (?P<zalozba>.*?)</li>']
    for i in range(10):
        rx = re.compile(rx_list[i], re.DOTALL)
        data = re.search(rx, ad)
        if data != None:
            dic = data.groupdict()
            for i in dic:
                if i == "leto_izdaje":
                    if len(dic[i]) > 4:
                        dic[i] = dic[i][-4:]
                    c = spremen(dic[i])
                    if c:
                        dic[i] = int(c)
                    else:
                        dic[i] = 0
                if i == "stevilo_strani":
                    c = spremen(dic[i])
                    if c:
                        dic[i] = int(c)
                    else:
                        dic[i] = 0
                if i == 'cena_v_evrih':
                    c = dic[i][:-2].replace(',', '.')
                    dic[i] = float(c)
                if i == 'vezava':
                    if dic[i] in 'Trdatrda':
                        dic[i] = 'trda'
                    elif dic[i] in 'Žepna knjiga žepna knjiga':
                        dic[i] = 'žepna'
                    elif dic[i] in 'Bro&scaron;iranaBro&scaron;iranobro&scaron;iranabro&scaron;irano':
                        dic[i] = 'broširana'
                    elif dic[i] in 'Mehkamehka':
                        dic[i] = 'mehka'
            dictionary[i] = dic[i]
        else:
            dictionary[tab[i]] = 0
    return dictionary



#seznam slovarjev podatkov z ene strani
def page_to_dicts(directory, filename):
    page = read_file_to_string(directory, filename)
    ads = page_to_ads(page)
    dic = [0 for i in range(len(ads))]
    for i in range(len(ads)):
        dic[i] = make_a_dictionary(ads[i])
    return dic


#pobere podatke z vseh strani in jih shrani v seznam slovarjev
def get_all_dicts():
    dicts = []
    for i in range(1, 21):
        dic = page_to_dicts(romani_directory_new, page_filename_new + '{}.html'.format(i))
        dicts += dic
    return dicts


#dobljeni podatki
##############################################################################################################


#napise csv
def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None


#napise dejanski csv romanov
def write_csv_romani():
    write_csv(keys, get_all_dicts(), csv_directory, csv_filename)

write_csv_romani()

##############################################################################################################

def no_repeated_rows():
    new_rows = []
    with open('csv_podatki/romani.csv', 'r', encoding='utf8') as in1:
        titles = []
        for line in in1:
            try:
                title = line.split(',')[1]
                if title not in titles:
                    titles.append(line.split(',')[1])
                    new_rows.append(line)
            except IndexError:
                pass
    with open('csv_podatki/romani.csv', 'w', encoding='utf8') as out1:
        for line in new_rows:
            out1.write(line)

no_repeated_rows()  