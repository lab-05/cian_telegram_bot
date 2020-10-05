# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 22:45:47 2020

@author: dmitrixsha
"""
import requests
import json
from lxml import html
import dataset
import datetime
import browser_cookie3

cookiejar = browser_cookie3.firefox(domain_name='cian.ru')


urlfile = 'url.txt'

def get_url(urlfile):
    with open(urlfile) as urlfiletxt:
        url = urlfiletxt.read()
    return url

url = get_url(urlfile)

db = dataset.connect('sqlite:///cian.db')
table = db.get_table('koptevo')


user_agent = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}

def getrequest(url):
    responses = requests.get(url, headers = user_agent, cookies=cookiejar)
    html1 = responses.text
    tree = html.fromstring(html1)
    return html1, tree


def get_json():
    result_to_json = getrequest(url)
    start_json_template = "window._cianConfig['frontend-serp'] = "
    if start_json_template in result_to_json[0]:    
        start = result_to_json[0].index(start_json_template) + len(start_json_template)
        end = result_to_json[0].index('</script>', start)
        json_raw = result_to_json[0][start:end].strip()[:-1]
        json1 = json.loads(json_raw)
        return json1    


def checknum():
    tmp_data_json = get_json()
    for i in range(len(tmp_data_json)):
        if tmp_data_json[i]['key'] == 'initialState':
            return i
            break
    

def get_urls(inf):
    for flat in inf[checknum()]['value']['results']['offers']:
        nowtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        id_flat = flat['id']
        url_flat = flat['fullUrl']
        price_flat = flat['bargainTerms']['price']
        place_flat= flat['geo']['userInput']
        table.insert_ignore(dict(CianId=id_flat, Url=url_flat, price=price_flat, Location=place_flat, Date=nowtime), ['CianId'])