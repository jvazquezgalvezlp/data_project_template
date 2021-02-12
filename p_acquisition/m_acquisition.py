from sqlalchemy import create_engine
import pandas as pd
import requests
from bs4 import BeautifulSoup

def import_databases(path):

    print('getting tables db...')
    conn_str = f'sqlite:///{path}'
    engine = create_engine(conn_str)

    print(f'getting data from {path}')
    query1 = 'SELECT * FROM career_info'
    career_info = pd.read_sql_query(query1, engine)

    query2 = 'SELECT * FROM country_info;'
    country_info = pd.read_sql_query(query2, engine)

    return country_info,career_info

def df_api(career_info):

    print('getting api info')
    list_api = []
    list_job_code = set(career_info['normalized_job_code'])
    for i in list_job_code:
        response = requests.get(f'http://api.dataatwork.org/v1/jobs/{i}')
        result_jobs = response.json()
        list_api.append(result_jobs)

    data_jobs = pd.DataFrame(list_api)

    return data_jobs

def df_webscraping():

    print('getting web info')

    url = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    country_codes = soup.find_all('td')

    return country_codes

