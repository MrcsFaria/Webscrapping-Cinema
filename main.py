from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument(f"--window-size=1920,1080")

#Input para o usuário falar qual filme ele quer buscar os horários
print("Qual filme você deseja buscar os horários de exibição?")
filme = input()

#Cinemas de SJC - SP são: Kinoplex, Cinépolis e Cinemark

def pegar_horarios_kinoplex():
    global df_kinoplex
    filme_kinoplex = filme.upper()
    url_kinoplex = "https://www.kinoplex.com.br/cinema/kinoplex-vale-sul/35"

    horarios_kinoplex = []

    id_div_cab = 0
    status = ""

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_kinoplex)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div/div/div/button'))
    )

    driver.find_element(By.XPATH, '/html/body/div[8]/div/div/div/button').click()

    for i_cab_1 in range(1, 11):
        try:
            xpath_cabecalho = f"/html/body/div[6]/div/div[1]/div[3]/div[{i_cab_1}]/div/div[1]/h4/a"

            filme_cabecalho = driver.find_element(By.XPATH, xpath_cabecalho).text

            if filme_cabecalho == filme_kinoplex:
                id_div_cab = i_cab_1
                status = "encontrado"
        except NoSuchElementException:
            pass

    if status == "encontrado":
        for i_div_1 in range(1, 11):
            try:
                for i_div_2 in range(0, 30, 2):
                    try:
                        xpath_p_horario = f"/html/body/div[6]/div/div[1]/div[3]/div[{id_div_cab}]/div/div[{i_div_1}]/span/ul/li[{i_div_2}]/span"

                        horario = driver.find_element(By.XPATH, xpath_p_horario).text

                        horarios_kinoplex.append(horario)
                    except NoSuchElementException:
                            pass
            except NoSuchElementException:
                pass
        print("Coleta dos Horários do Kinoplex Finalizada")
    else:
        print("Filme não encontrado no Kinoplex")

    df_kinoplex = pd.DataFrame(horarios_kinoplex, columns=['Horários Kinoplex'])

    driver.quit()

def pegar_horarios_cinepolis():
    global df_cinepolis
    url_cinepolis = "https://www.cinepolis.com.br/programacao/sao+jose+dos+campos/68.html"
    id_div_cab = 0
    status = ""
    filme_cinepolis = filme.title()
    horarios_cinepolis = []

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_cinepolis)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[8]/div/a'))
    )

    driver.find_element(By.XPATH, '/html/body/div[4]/div[8]/div/a').click()

    for i_cab_1 in range(1, 11):
        try:
            xpath_cabecalho = f"/html/body/div[4]/div[5]/section[1]/section[2]/div[5]/div/div/div/article[{i_cab_1}]/div/header/h3/a"

            filme_cabecalho = driver.find_element(By.XPATH, xpath_cabecalho).text

            if filme_cabecalho == filme_cinepolis:
                id_div_cab = i_cab_1
                status = "encontrado"
        except NoSuchElementException:
            pass

    if status == "encontrado":
        for i_div_1 in range(0, 11):
            try:
                for i_div_2 in range(0, 20):
                    try:
                        xpath_p_horario = f"/html/body/div[4]/div[5]/section[1]/section[2]/div[5]/div/div/div/article[{id_div_cab}]/div/div[{i_div_1}]/div/div[2]/time[{i_div_2}]/a"

                        horario = driver.find_element(By.XPATH, xpath_p_horario).text

                        horarios_cinepolis.append(horario)
                    except NoSuchElementException:
                        pass
            except NoSuchElementException:
                pass
        print("Coleta dos Horários do Cinépolis Finalizada")
    else:
        print("Filme Não Encontrado no Cinépolis")

    df_cinepolis = pd.DataFrame(horarios_cinepolis, columns=['Horários Cinepolis'])

    driver.quit()

def pegar_horarios_cinemark():
    global df_cinemark
    filme_cinemark = filme.replace(" ", "-").lower()
    url_cinemark = f"https://www.cinemark.com.br/filme/{filme_cinemark}"

    horarios_cinemark = []

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_cinemark)

    img = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section[1]/div/div/img'))
    )
        
        # Pegando o atributo 'alt' da imagem
    alt_text = img.get_attribute('alt')

    if alt_text == "Imagem não encontrada":
            print("Filme Não Encontrado no Cinemark")
    else:        
        WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div/div[17]/div/label/input'))
        )

        driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div/div[17]/div/label').click()

        WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/footer/div/button'))
        )

        driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/footer/div/button').click()

        WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div/div[5]/div[1]/div[2]/label/input'))
        )

        driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div/div[5]/div[1]/div[2]/label').click()

        WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/footer/div/button'))
        )

        driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/footer/div/button').click()

        WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/section[3]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div[1]/p'))
        )

        for i_div_1 in range(1, 11):
            try:
                for i_div_2 in range(1, 11):
                    try:
                        xpath_p_horario = f"/html/body/div[3]/section[3]/div/div[2]/div[2]/div[1]/div[2]/div[{i_div_1}]/div[2]/div/div/div/div/div[{i_div_2}]/p"

                        horario = driver.find_element(By.XPATH, xpath_p_horario).text

                        horarios_cinemark.append(horario)
                    except NoSuchElementException:
                        pass
            except NoSuchElementException:
                pass
        print("Coleta dos Horários do Cinemark Finalizada")
            
        
    df_cinemark = pd.DataFrame(horarios_cinemark, columns=['Horários Cinemark'])
    driver.quit()

pegar_horarios_cinemark()

sleep(2)

pegar_horarios_cinepolis()

sleep(2)

pegar_horarios_kinoplex()

sleep(2)

arquivo_excel = f'horarios - {filme}.xlsx'

if not df_cinemark.empty or not df_cinepolis.empty or not df_kinoplex.empty:
    with pd.ExcelWriter(arquivo_excel, engine='openpyxl') as writer:
        if not df_cinemark.empty:
            df_cinemark.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=0, index=False)
        if not df_cinepolis.empty:
            df_cinepolis.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=1, index=False)
        if not df_kinoplex.empty:
            df_kinoplex.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=2, index=False)

    print(f"Horários coletados e salvos no arquivo: {arquivo_excel}")
else:
    print("Não foram encontrados horários do filme informado para hoje. Nenhum arquivo foi criado.")

