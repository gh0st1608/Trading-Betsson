import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",chrome_prefs)

driver = webdriver.Chrome(options = chrome_options)

link = 'https://www.apuestatotal.com/apuestas-deportivas/#/sport/66/livenow'
driver.get(link)

ligas_xpath = '//div[@class = "_asb_simple-button _asb_simple-button-container-block _asb_simple-button-pointer  _asb_top-leagues-item "]'
ver_todo_xpath = '//div[@class = "_asb_expansion-panel  _asb_events-tree-table-node-CH "]'
partidos_xpath = './/div[@class = "asb-flex"]'
equipos = './/div[@class = "_asb_events-table-row-competitor-name "]'
scores = './/div[@class = "asb-flex-cc asb-unshrink _asb_price-block-content-price "]'


dicc = {'liga':[],
        'equipo_local' : [],
        'equipo_visita' : [],
        'cuota_gana_local' : [],
        'couta_empata':[],
        'cuota_gana_visita' : []}

time.sleep(5)
lista_ligas = driver.find_elements(By.XPATH, ligas_xpath)

for l in range(len(lista_ligas)-4):
    lista_ligas[l].click()
    
    t = 0
    while t < 6:
        try: #
            time.sleep(1)
            driver.find_element(By.XPATH, ver_todo_xpath)
            print('La página terminó de cargar')
            t = 0
            break
        except:
            time.sleep(3)
            t += 1
            print('La página está cargando')
            
    time.sleep(3)
    partidos = driver.find_elements(By.XPATH, partidos_xpath)
    for i in range(len(partidos)-1):
        try:
            e_local = partidos[i+1].find_elements(By.XPATH, equipos)[0].text
            e_visita = partidos[i+1].find_elements(By.XPATH, equipos)[1].text
            score_1 = partidos[i+1].find_elements(By.XPATH, scores)[0].text
            score_2 = partidos[i+1].find_elements(By.XPATH, scores)[1].text
            score_3 = partidos[i+1].find_elements(By.XPATH, scores)[2].text
                
            dicc['liga'].append(lista_ligas[l].text)
            dicc['equipo_local'].append(e_local)
            dicc['equipo_visita'].append(e_visita)
            dicc['cuota_gana_local'].append(score_1)
            dicc['couta_empata'].append(score_2)
            dicc['cuota_gana_visita'].append(score_3)
        except Exception as e:
            print(e)
            print('Error de Carga')
    
#driver.close()
data = pd.DataFrame(dicc)
print(data)