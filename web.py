import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time


def downloader(url_1, name_final, pag):
    pag.get(f'https://9xbuddy.com/process?url={url_1}')

    time.sleep(6)
    divs = pag.find_elements(By.XPATH,'//div[contains(@class, "lg:flex")]//div[contains(text(), "1080")]')

    # Itera sobre los elementos div que contienen '1080'
    for div in divs:
        # Encuentra el elemento padre que contiene el enlace ('a') deseado
        parent_element = div.find_element(By.XPATH,'ancestor::div[contains(@class, "lg:flex")]')

        # Encuentra el enlace ('a') dentro del elemento padre
        link = parent_element.find_element(By.XPATH,'.//a')

        # Obtiene el atributo href del enlace
        link_href = link.get_attribute('href')
        # Imprime el texto '1080' y el href del enlace
        enlace_sin_parte = link_href.split('?')[0]
        urls_final = f"{enlace_sin_parte}?ext=mp4&customName={name_final}"

        # Reemplazar el atributo href del enlace con el nuevo enlace modificado
        pag.execute_script(f"arguments[0].setAttribute('href', '{urls_final}')", link)
        time.sleep(3)
        link.click()
        time.sleep(3)



def conseguir_links (url_2 , drive ):
    req = Request(url_2, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}) # Adding a User-Agent header to the request
    response = urlopen(req).read()

    cuevana_serie_page_soup = BeautifulSoup(response, 'html.parser')

    # Encontrar todos los elementos <li> con la clase "clili" que tienen los atributos data-type="13" y data-video
    elements_with_data = cuevana_serie_page_soup.find_all('li', {'class': 'clili', 'data-type': '13', 'data-video': True})

    # Imprimir los valores de data-type y data-video
    for element in elements_with_data:
        data_video_value = element.get('data-video')
        span_text = element.find('span', class_='cdtr').text.strip() if element.find('span', class_='cdtr') else None
        print(f" url del video: {data_video_value}")
        if span_text:
            parts = span_text.split(' - ')
            middle_part = parts[1]
            print(f"idioma : {middle_part}")
            # Dividir la URL por "/"
            parts = url_2.split('/')

            # Obtener el texto después de "episodio"
            text_after_episode = parts[-1]

            nombre_final = f"{text_after_episode}-{middle_part}"
            downloader(data_video_value, nombre_final, drive)


chrome_options = Options()
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#chrome_options.add_argument('--headless')


service = Service(ChromeDriverManager().install())
driver = uc.Chrome(service=service,options=chrome_options)


################### variables ###############


link_original ="https://cuevana3.ch/serie/the-walking-dead"

season_n  = 1

##################################


driver.get(link_original)

time.sleep(3)


# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source,"html.parser")

# Find all elements that contain the seasons
season_1 = soup.find("ul", {"id": f"season-{id}"})

if season_1:
    # Find all <a> elements within the season_1 element
    episode_links = season_1.find_all("a", href=True)

    # Extract href attributes from the <a> elements and add prefix
    hrefs = [f"https://cuevana3.ch{link['href']}" for link in episode_links]

    with open('capitulos.txt', 'w') as archivo:
        for href_1 in hrefs:
            archivo.write(href_1 + '\n')
else:
    print(f"No se encontró la temporada {season_n}")
    driver.quit()


with open('capitulos.txt', 'r') as archivo:
    # Lee cada línea del archivo
    for linea in archivo:
        # Procesa la línea (en este caso, solo imprime el enlace)
        enlace = linea.strip()  # Elimina espacios en blanco al inicio y final de la línea
        print(f"Procesando enlace: {enlace}")
        conseguir_links (enlace , driver )
