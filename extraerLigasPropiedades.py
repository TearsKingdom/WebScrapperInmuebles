from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import math 

muestra = 20 #Número de tarjetas que se muestran por página
link = "https://www.inmuebles24.com/departamentos-en-renta-en-miguel-hidalgo"
delay = 3000 #Delay en milisegundos para cerrar y abrir página
with sync_playwright() as p:
    browser = p.chromium.launch(headless= False)
    page = browser.new_page()
    page.goto(link+'.html')
    soup = bs(page.content(), 'html.parser')

    #Calculamos el número de páginas que hay para esta búsqueda
    numero_pags = soup.find('h1').text
    numero_pags = numero_pags[0:numero_pags.find(' ')]
    numero_pags = math.ceil(int(numero_pags.replace(',',''))/muestra)
    #Crea la lista con los links de las propiedades
    
    propiedades = ['https://www.inmuebles24.com'+i["data-to-posting"] for i in soup.find_all("div") if i.has_attr( "data-to-posting")]
    #Se añade abase de datos

    page.wait_for_timeout(delay)
    page.close()
    
    for i in range(2,numero_pags):
        page = browser.new_page()
        page.goto(link+f'pagina-{i}.html')
        soup = bs(page.content(), 'html.parser')
        propiedades = ['https://www.inmuebles24.com'+i["data-to-posting"] for i in soup.find_all("div") if i.has_attr( "data-to-posting")]
        #Se añade abase de datos

        #Delay (hay que medir cuánto)
        page.wait_for_timeout(delay)
        page.close()
    
    browser.close()

