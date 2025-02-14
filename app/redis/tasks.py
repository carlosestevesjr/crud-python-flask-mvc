from selenium import webdriver
from selenium.webdriver.common.by import By
from app.redis.celery_config import celery
from app.models.Forecast import Location, Forecast, Astro
from app import create_app  # Supondo que você tenha uma função create_app() para inicializar o app

from app.models.Item import Item
from app import db
import json
import pandas as pd
import time
import random

import os
import shutil

from uuid import uuid4
from datetime import datetime, timedelta

def init_tasks():
    # Importa as funções de tarefas aqui, evitando o problema de circularidade
    from app.redis.tasks import process_task, fetch_article_titles
    return {"process_task": process_task, "fetch_article_titles": fetch_article_titles}

# Função recursiva que retorna um dicionário com os dados mapeados
def map_json(data, parent_key=''):
    result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            result.update(map_json(value, new_key))  # Atualiza o resultado com os dados aninhados
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{parent_key}[{i}]"
            result.update(map_json(item, new_key))  # Atualiza o resultado com os dados da lista
    else:
        result[parent_key] = data

    return result

@celery.task(name="app.redis.tasks.process_task")  # Caminho atualizado
def process_task(x, y):
    return x + y

@celery.task(name="app.redis.tasks.fetch_article_titles")
def fetch_article_titles():
    # Aguarda até conseguir o lock (evita concorrência)
    print("Iniciando a captura do título...") # Verifique se isso aparece
    options = webdriver.ChromeOptions()
    id = uuid4()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-data-dir={os.getcwd()}/chromeprofiles/{id}")
    options.add_argument(f"--profile-directory=chromeprofile")

    driver = webdriver.Chrome(options=options)


    # Data de referência: 14 dias à frente da data atual
    data_referencia = datetime.now() + timedelta(days=14)
    print(data_referencia)
    # Lista para armazenar as datas
    datas = []

    # Lista para armazenar as datas dos últimos 15 dias a partir da data de referência
    for i in range(5):
        data_formatada = (data_referencia + timedelta(days=i)).strftime('%Y-%m-%d')
        datas.append(data_formatada)

        print(f"http://api.weatherapi.com/v1/future.json?key=f6979f9116174953a9e135306250702&q=Curitiba&dt={data_formatada}")
        driver.get(f"http://api.weatherapi.com/v1/future.json?key=f6979f9116174953a9e135306250702&q=Curitiba&dt={data_formatada}")

        # Obtém o conteúdo da página
        page_content = driver.find_element(By.TAG_NAME, 'pre').text

        # Carrega o conteúdo JSON
        dados = json.loads(page_content)

        data_final = map_json(dados)

        # Exibe os dados obtidos
        print(data_final)
    
        # Espera entre 3 e 7 segundos antes da próxima requisição
        time.sleep(random.uniform(0, 5))

        # # Criando e salvando uma localização
        # location = Location(
        #     name=data_final['location.name'], 
        #     region=data_final['location.region'], 
        #     country=data_final['location.country'], 
        #     lat=data_final['location.lat'], 
        #     lon=data_final['location.lon'], 
        #     tz_id=data_final['location.tz_id'], 
        #     localtime_epoch=data_final['location.localtime_epoch'], 
        #     localtime=data_final['location.localtime']
        # )
        # db.session.add(location)
        # db.session.commit()


        # # Criando e salvando uma previsão
        # forecast = Forecast(
        #     location_id=location.id, 
        #     date="2025-03-02", 
        #     date_epoch=1740873600, 
        #     maxtemp_c=24.8, 
        #     maxtemp_f=76.6, 
        #     mintemp_c=17.3, 
        #     mintemp_f=63.1, 
        #     avgtemp_c=20.3, 
        #     avgtemp_f=68.5, 
        #     maxwind_mph=6.5, 
        #     maxwind_kph=10.4, 
        #     totalprecip_mm=2.7, 
        #     totalprecip_in=0.11, 
        #     avgvis_km=6.1, 
        #     avgvis_miles=3, 
        #     avghumidity=87, 
        #     condition_text="Moderate or heavy rain shower", 
        #     condition_icon="//cdn.weatherapi.com/weather/64x64/day/356.png", 
        #     uv=6
        # )
        # forecast.save()

        # # Criando e salvando dados astronômicos
        # astro = Astro(
        #     forecast_id=forecast.id, 
        #     sunrise="06:12 AM", 
        #     sunset="06:46 PM", 
        #     moonrise="08:47 AM", 
        #     moonset="08:33 PM", 
        #     moon_phase="Waxing Crescent", 
        #     moon_illumination=6
        # )
        # astro.save()


        # forecast = Forecast(
        #     name="Previsão A",
        #     description="Descrição da previsão"
        # )

        # Forecast.save()

        # # Salva os dados em um arquivo Excel com um nome único a cada iteração
        # df = pd.json_normalize(map_json(dados))  # Caso o retorno seja um JSON simples
        # nome_arquivo = f"dados_climaticos_{data_formatada}.xlsx"
        # df.to_excel(nome_arquivo, index=False)

    
    print(datas)
    # Fecha o driver
    driver.quit()

    # Defina o caminho da pasta que deseja remover
    pasta = f'chromeprofiles/{id}'

    # Verifica se a pasta existe
    if os.path.exists(pasta):
        shutil.rmtree(pasta)
        print(f"Pasta '{pasta}' removida com sucesso.")
    else:
        print("A pasta não existe.")

    print("fim a captura do título...")  # Verifique se isso aparece

    return []

