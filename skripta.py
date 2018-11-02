import requests
import re
import os
import csv

romani_url = 'http://felix.si/50-romani?n=54&id_category=50'
romani_directory = 'podatki'
romani_directory_new = 'novi_podatki'
page_filename = 'page'  #.html
csv_filename = 'romani.csv'


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


##############################################################################################################


#prebere stran v filename-u v mapi directory
def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        #print('sem v read_file_to_string({}, {})'.format(directory, filename))
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
            print(l)
            linki_romanov.add(l[6:-1])
    print('**************************************************************', len(linki_romanov))
    return linki_romanov


#skombinira html-je z linkov neke strani
def save_links_to_file(list_of_links, directory, filename):
    text = ''
    for i in list_of_links:
        #print(i)
        text += download_url_to_string(i)
    save_string_to_file(text, directory, filename)


#shrani 20 skombiniranih html-jev 
def new_html_files():
    for i in range(1, 21):
        links = find_links(romani_directory, 'page{}.html'.format(i))
        save_links_to_file(links, romani_directory_new, 'new_page{}.html'.format(i))


##############################################################################################################


#razdeli nove html-je na posamezne knjige
def page_to_ads(page):
    #read_file_to_string(directory, filename)
    rx = re.compile(r'<!DOCTYPE.*?</html>',
                    re.DOTALL)
    ads = re.findall(rx, page)
    return len(ads)  #odstrani 'len'
