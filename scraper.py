import sys
from time import sleep
from selenium import webdriver

import requests
from requests_html import HTMLSession, AsyncHTMLSession
from selenium.common.exceptions import NoSuchElementException
from w3lib import form


def init_session():
    main_url = "https://comparador.cnmc.gob.es"

    session = HTMLSession()
    print("Sesion iniciada")
    return session, main_url

def get_page(session, url):
    page = session.get(url)
    return page

"""
def contract_selector(main_page, url_comparator):
    return form_page, url_form


#def entry_form(form_page):
    return data_page, url_data


#def data_extract(data_page):
    return data

"""


def main():
    session, main_url = init_session()
    main_page = get_page(session, main_url)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)