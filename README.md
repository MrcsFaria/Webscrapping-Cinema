# Webscrapping - Sistema de Coleta de Horários de Filme

Este projeto é um sistema de web scraping desenvolvido em Python, que coleta os horários de exibição de filmes em três cinemas de São José dos Campos, SP: Kinoplex, Cinépolis e Cinemark. O usuário informa o nome do filme desejado, e o sistema busca os horários de exibição nos sites desses cinemas, salvando os resultados em um arquivo Excel.

## Funcionalidades

- Coleta de Horários de Filmes: Coleta os horários de exibição de um filme informado pelo usuário nos cinemas Kinoplex, Cinépolis e Cinemark em São José dos Campos, SP.
- Geração de Arquivo Excel: Salva os horários coletados em um arquivo Excel para fácil consulta e análise.


## Tecnologias Utilizadas
- Python: Linguagem de programação principal utilizada no projeto.

## Bibliotecas Python:
  - time: Para manipulação de tempo e pausas no script.
  - pandas: Para manipulação e análise de dados, além de criação do arquivo Excel.
  - selenium: Para automação de navegação web e coleta de dados.
  - webdriver: Para controle do navegador Google Chrome.
  - openpyxl: Para manipulação de arquivos Excel.

## Como Executar
Pré-requisitos: Python

```bash
# clonar repositório
git clone https://github.com/MrcsFaria/Webscrapping-Cinema

# Navegue até o diretório do projeto:
cd Webscrapping-Cinema

Certifique-se de ter o [WebDriver do Chrome](https://sites.google.com/chromium.org/driver/) instalado e configurado no PATH do sistema.

# Instale as dependências necessárias
pip install pandas selenium openpyxl

# executar o projeto
python main.py

Informe o nome do filme quando solicitado
```

## Código de Exemplo

Aqui está uma amostra do código do projeto:

```python
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

print("Qual filme você deseja buscar os horários de exibição?")
filme = input()

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
```
# Planilha Gerada

![Exemplo de funcionamento](https://github.com/MrcsFaria/Webscrapping-Cinema/blob/main/Prints/1.PNG)

# Autor

Marcos Vinicius Faria

https://br.linkedin.com/in/marcos-vinicius-faria-124266186
