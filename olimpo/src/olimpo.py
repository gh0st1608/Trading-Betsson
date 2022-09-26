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
#chrome_prefs["profile.default_content_settings"] = {"images": 2}

"""
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--start-maximized')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')

options.add_argument('--disable-notifications')
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
"""
driver = webdriver.Chrome(options = chrome_options)

link = 'https://www.olimpo.bet/#home'
driver.get(link)
lista_xpath = '//div[@class = "KambiBC-sandwich-filter-foreground KambiBC-sandwich-filter-foreground--level-1"]'
tipo_xpath = './/ul[@class = "KambiBC-filter-menu"]/li'    
partidos_xpath = '//ul[@class = "KambiBC-sandwich-filter__list"]/li'      
equipos_xpath = './/div[@class = "KambiBC-event-participants"]/div'
score_xpath = './/div[@class = "KambiBC-bet-offer__outcomes"]/button'

dicc = {'tipo':[],
        'equipo_local' : [],
        'equipo_visita' : [],
        'cuota_gana_local' : [],
        'couta_empata':[],
        'cuota_gana_visita' : []}

t = 0
while t < 6:
    try: #
        lista = driver.find_element(By.XPATH, lista_xpath)
        t = 0
        break
    except:
        time.sleep(3)
        t += 1
        print('La página está cargando')

    


for i in range(len(lista.find_elements(By.XPATH, tipo_xpath))):
    try:
        t = lista.find_elements(By.XPATH, tipo_xpath)[i]
        t.click()
        
        time.sleep(1.5)
        tipo = lista.find_elements(By.XPATH, tipo_xpath)[i].text                
        partidos = driver.find_elements(By.XPATH,partidos_xpath)
        
        for j in range(1,len(partidos)+1):
            try:
                e_local = partidos[j-1].find_elements(By.XPATH,equipos_xpath)[0].text
                e_visita = partidos[j-1].find_elements(By.XPATH,equipos_xpath)[1].text
                score_1 = partidos[j-1].find_elements(By.XPATH, score_xpath)[0].text
                score_2 = partidos[j-1].find_elements(By.XPATH, score_xpath)[1].text
                score_3 = partidos[j-1].find_elements(By.XPATH, score_xpath)[2].text
                
                dicc['tipo'].append(tipo)
                dicc['equipo_local'].append(e_local)
                dicc['equipo_visita'].append(e_visita)
                dicc['cuota_gana_local'].append(score_1)
                dicc['couta_empata'].append(score_2)
                dicc['cuota_gana_visita'].append(score_3)
            except:
                print('error partido')
                pass
    except:
        print('Error en tipo')
        try:
            driver.find_element(By.XPATH, '//a[@class = "ico--cierre"]').click()
        except:
            pass
        pass
driver.close()
data = pd.DataFrame(dicc)

print(data)
fpath = Path('olimpo.py').absolute()
print(fpath)
data.to_excel(r'./data/data.xlsx',index = False)

