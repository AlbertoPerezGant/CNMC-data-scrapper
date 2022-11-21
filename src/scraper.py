# Importación de liberías
import pandas as pd
from time import sleep
import sys

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By # Para poder usar el By


#Inicialización driver
def init_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


#Cierre driver
def close_driver(driver):
    driver.close()


#Aceptación cookies
def accept_cookies(driver):
    driver.find_element(By.CLASS_NAME,'cookiesjsr-btn.important').click()


#Abrir lista de opciones
def selecct_sum(driver):
    driver.find_element(By.ID, "input-47").click()


#Selección de ofertas de electricidad en desplegable
def select_elect(driver):
    driver.find_element(By.ID, "list-item-59-0").click()


#Selección de ofertas de gas en desplegable
def select_gas(driver):
    driver.find_element(By.ID, "list-item-59-1").click()


#Selección de ofertas conjuntas en desplegable
def select_both(driver):
    driver.find_element(By.ID, "list-item-59-2").click()


#Selección de boton "Iniciar"
def iniciar(driver):
    driver.find_element(By.ID, "Iniciar").click()


#Escribe un código postal en formulario electricidad
def type_postal_code(driver):
    driver.find_element(By.NAME, "codigoPostal").click()
    driver.find_element(By.NAME, "codigoPostal").send_keys("08035")


#Continúa desde el formulario hasta la siguiente página
def continue_to_page(driver, gas=False):
    driver.find_element(By.ID, "Continuar").click()
    sleep(1)

    if gas == False:
        driver.find_element(By.CLASS_NAME, "v-input--selection-controls__ripple").click()
        sleep(1)
        driver.find_element(By.XPATH, "(.//*[normalize-space(text()) and normalize-space(.)='He leído este aviso'])[1]/following::span[2]").click()
        return driver

    else: return driver


#Navegación hasta página de ofertas de electricidad
def get_comparator_elect(url_base):
    driver = init_driver(url_base)
    accept_cookies(driver)
    selecct_sum(driver)
    select_elect(driver)
    iniciar(driver)
    sleep(3)
    type_postal_code(driver)
    driver = continue_to_page(driver)
    return driver


#Naveción hasta página de gas
def get_comparator_gas(url_base):
    driver = init_driver(url_base)
    accept_cookies(driver)
    selecct_sum(driver)
    select_gas(driver)
    iniciar(driver)
    sleep(3)
    type_postal_code(driver)
    driver = continue_to_page(driver, gas=True)
    return driver


#Naveción hasta página de ofertas combinadas
def get_comparator_both(url_base):
    driver = init_driver(url_base)
    accept_cookies(driver)
    selecct_sum(driver)
    select_both(driver)
    iniciar(driver)
    sleep(3)
    type_postal_code(driver)
    continue_to_page(driver)
    return driver


#Extraccion de tabla de ofertas de electricidad
def get_elect_table(driver):

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all('table', attrs={'class': ''})
    
    for table in tables[1]:

        rows = table.find_all('tr', attrs={'class': ''})
        table_list = []

        for row in rows:

            data = row.find_all('td')
            row_list = []

            for elem in data:
                #Extraccion de cada elemento de cada fila y adicion a row_list

                if data[0] == elem:

                    company = elem.find('img').attrs['alt']
                    row_list.append(company)
                elif data[1] == elem:

                    oferta = row.find('a').text.lstrip()
                    row_list.append(oferta)
                elif data[5] == elem:

                    servicios_adicionales = elem.find('div').string
                    row_list.append(servicios_adicionales)
                elif data[7] == elem:

                    eco = elem.find('i').attrs['class'][-1]

                    if eco == 'grey--text':
                        row_list.append(False)
                    elif eco == 'green--text':
                        row_list.append(True)
                elif data[8] == elem:
                    break
                else:
                    row_list.append(elem.string)

            table_list.append(row_list)

    #Conversión a dataframe
    df_elect = pd.DataFrame(table_list)
    df_elect.columns = ['Comercializadora', 'Oferta', 'Importe primera factura', 
    'Importe siguientes facturas', 'Validez', 'Servicios adicionales', 'Penalizacion', 'Verde']
    
    return df_elect


#Extraciión de tabla de ofertas conjuntas
def get_both_table(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all('table')

    for table in tables[0]:

        rows = table.find_all('tr', attrs={'class': ''})
        table_list = []
        for row in rows:

            data = row.find_all('td')
            row_list = []

            for elem in data:
                #Extraccion de cada elemento de cada fila y adicion a row_list
                if data[0] == elem:

                    company = elem.find('img').attrs['alt']
                    row_list.append(company)
                elif data[1] == elem:

                    oferta = row.find('a').text.lstrip()
                    row_list.append(oferta)
                elif data[5] == elem:

                    servicios_adicionales = elem.find('div').string
                    row_list.append(servicios_adicionales)
                elif data[7] == elem:

                    eco = elem.find('i').attrs['class'][-1]

                    if eco == 'grey--text':
                        row_list.append(False)
                    elif eco == 'green--text':
                        row_list.append(True)
                elif data[8] == elem:
                    break
                else:
                    row_list.append(elem.string)
            
            table_list.append(row_list)

    #Conversión a dataframe        
    df_both = pd.DataFrame(table_list)
    df_both.columns = ['Comercializadora', 'Oferta', 'Importe primer año', 
    'Importe 2o año', 'Validez', 'Servicios adicionales', 'Penalizacion', 'Verde']

    return df_both


#Extraciión de tabla de gas
def get_gas_table(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find_all('tbody', attrs={'class': ''})
    head = soup.find_all('thead', attrs={'class': 'v-data-table-header'})

    for table in head:
        rows = table.find_all('th')
        headers_list = []

        for row in rows:
            headers = row.find('span').text
            headers_list.append(headers)

    for table in body:
        rows = table.find_all('tr', attrs={'class': ''})
        table_list = []

        for row in rows:
            row_list = []
            data = row.find_all('td',attrs={'class': 'text-center'})

            for elem in data:
                #Extraccion de cada elemento de cada fila y adicion a row_list
                if data[0] == elem:
                    if elem.find('img'):
                        company = elem.find('img')['alt']
                        row_list.append(company)
                    else:
                        company = elem.find('p').text.lstrip().rstrip()
                        row_list.append(company)
                elif data[1] == elem:
                        oferta = elem.find('a').text.lstrip().rstrip()
                        row_list.append(oferta)
                elif data[2] == elem:
                        price = elem.find('p').text.lstrip().rstrip()
                        row_list.append(price)
                elif data[3] == elem:
                        price_2 = elem.find('div').text.lstrip().rstrip()
                        row_list.append(price_2)
                elif data[4] == elem:
                        validez = elem.find('div').text.lstrip().rstrip()
                        row_list.append(validez)
                elif data[5] == elem:
                        servicios_adicionales = elem.find('div').text.lstrip().rstrip()
                        row_list.append(servicios_adicionales)
                elif data[6] == elem:
                        penality = elem.find('div').text.lstrip().rstrip()
                        row_list.append(penality)
                else:
                        row_list.append(elem.string)
            table_list.append(row_list)
    
    #Conversión a dataframe
    df_gas = pd.DataFrame(table_list)
    df_gas.columns= headers_list
    df_gas.drop(df_gas.columns[-1], axis=1, inplace=True)
    
    return df_gas


#Scraping CNMC ofertas electricidad
def elect_scrap(url_base):

    #Navegación hasta la página de ofertas de electricidad
    driver_elect = get_comparator_elect(url_base)
    sleep(5)

    #Obtencion del dataframe de ofertas de electricidad
    df_elect = get_elect_table(driver_elect)
    sleep(5)

    #Cierre de driver
    close_driver(driver_elect)
    return df_elect


#Scraping CNMC ofertas gas
def gas_scrap(url_base):

    #Navegación hasta la página de ofertas de gas
    driver_gas = get_comparator_gas(url_base)
    sleep(5)

    #Obtencion del dataframe de ofertas de gas
    df_gas = get_gas_table(driver_gas)
    sleep(5)

    #Cierre de driver
    close_driver(driver_gas)
    return df_gas


#Scraping CNMC ofertas conjuntas
def both_scrap(url_base):

    #Navegación hasta la página de ofertas conjuntas
    driver_both = get_comparator_both(url_base)
    sleep(5)

    #Obtencion del dataframe de ofertas conjuntas
    df_both = get_both_table(driver_both)
    sleep(5)

    #Cierre de driver
    close_driver(driver_both)
    return df_both


#Convierte dataframe a csv
def data2csv(df, name):
		
        df.to_csv(name, encoding='utf-8')


def main():

    # Definición de la url base
    url_base = 'https://comparador.cnmc.gob.es/'

    #Scraping de las diferentes opciones y obtención de un dataframe
    df_elect = elect_scrap(url_base)
    df_gas = gas_scrap(url_base)
    df_both = both_scrap(url_base)

    #Generacion de archivos csv
    data2csv(df_elect, 'comparador_electricidad.csv')
    data2csv(df_gas, 'comparador_gas.csv')
    data2csv(df_both, 'comparador_conjuntas.csv')   
    
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)