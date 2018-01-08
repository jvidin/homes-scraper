## http://altitudelabs.com/blog/web-scraping-with-python-and-beautiful-soup/
## https://www.blog.pythonlibrary.org/2014/02/26/python-101-reading-and-writing-csv-files/ -> list of dictionarys to csv

import csv
import logging
import re

import requests
from bs4 import BeautifulSoup

data = []


def url_fetcher(page_nr=1):
    # url example -> http://www.era.pt/imoveis/default.aspx?pg=1&o=1&q=Comprar%20almada&or=41&idioma=pt
    url = 'http://www.era.pt/imoveis/default.aspx?pg={}&o=1&q=Comprar%20almada&or=41&idioma=pt'.format(page_nr)
    page_load = requests.get(url)
    page_scanner(page_load, page_nr)


def page_scanner(page_load, page_nr):
    # url = 'http://www.era.pt/imoveis/default.aspx?pg={}&o=1&q=Comprar%20almada&or=41&idioma=pt'.format(page)
    # page = requests.get(url)
    id_scan = 0

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page_load.content, 'html.parser')

    # Take out the <div> of name and get its value
    for base in soup.find_all('div', {'class': 'blockLeft imovel js-open-show-imovel'}):
        # print(base.prettify())

        rec = {'id_scan': id_scan, 'id_page': page_nr}
        # Id
        try:
            ref_id = base.find('input').attrs['value']
            rec['ref_id'] = ref_id
            # print(id)
        except Exception as e:
            logging.exception(e)
            pass

        # Price
        try:
            price = base.find('span', class_='preco').span.text
            rec['price'] = price
        except Exception as e:
            e = e
            rec['price'] = 'sob consulta'
            pass

        # Local
        try:
            local = base.find('span', class_='openSansR t12 cinza17').text
            rec['local'] = local.replace(',\xa0', '')  # Replacing the strange string start.
            # print(local)
        except Exception as e:
            logging.exception(e)
            pass

        # Type Apartment
        try:
            ref_type = base.find('div', class_='tipo').text
            rec['ref_type'] = ref_type
            # print(ref_type)
        except Exception as e:
            logging.exception(e)
            pass

        # Link to ref
        try:
            link = base.find(id=re.compile("img_imovel$")).attrs['href']
            rec['link'] = 'http://www.era.pt' + link
            # print(link)
        except Exception as e:
            logging.exception(e)
            pass

        data.append(rec)
        rec['id_scan'] = len(data)
    print(len(data))


def write_csv(data):
    # print(scan_list)
    print('writing data for file ...')
    headers = [x for x in data[0].keys()]  # Getting keys as fieldnames from index 0 dictionary of list
    with open('almada.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def max_page(page=1):
    url = 'http://www.era.pt/imoveis/default.aspx?pg={}&o=1&q=Comprar%20almada&or=41&idioma=pt'.format(page)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for base in soup.find_all('div', class_='blockLeft footer'):
        # print(base.prettify())
        page_num = base.select('div a')
        # max_page = max([int(i.text) for i in page_num])
        print([int(i.text) if not (i.isspace() or i == '') else 0 for i in page_num])
        print(max_page)
        # for page in page_num:
        #     print(page.text)

    # Fetch de last page


if __name__ == "__main__":

    # max_page()
    # url_fetcher()
    # page_scanner()

    for i in range(1, 100):
        url_fetcher(i)
    write_csv(data)
