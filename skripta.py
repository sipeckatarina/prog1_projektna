import requests
import re
import os
import csv

romani_url = 'http://felix.si/50-romani?n=54&id_category=50'
# mapa, v katero bomo shranili podatke
romani_directory = 'podatki'
# ime datoteke v katero bomo shranili glavno stran
page_filename = 'page' #.html
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'romani.csv'

def download_url_to_string(url):
    '''This function takes a URL as argument and tries to download it
    using requests. Upon success, it returns the page contents as string.'''
    try:
        url_get = requests.get(url)
    except:
        return "Tole pa ni šlo."
    return url_get.text

def save_strings_to_files():
    def save_string_to_file(text, directory, filename):
        '''Write "text" to the file "filename" located in directory "directory",
        creating "directory" if necessary. If "directory" is the empty string, use
        the current directory.'''
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, filename)
        with open(path, 'w', encoding='utf-8') as file_out:
            file_out.write(text)
        return None
    for i in range(10, 21):
        if i == 1:
            save_string_to_file(download_url_to_string(romani_url), romani_directory, page_filename + '{}'.format(i) + '.html')
        else:
            save_string_to_file(download_url_to_string(romani_url + '&p={}'.format(i)), romani_directory, page_filename + '{}'.format(i) + '.html')
    return None
