# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 22:45:47 2020

@author: dmitrixsha
"""
import sqlite3
import pandas as pd
import datetime
def save_xls():
    cnx = sqlite3.connect('cian.db')

    df = pd.read_sql_query("SELECT * FROM cian_result", cnx)
    df = df[df['price']<=33100].sort_values(by=['price'])
    df.to_excel("cian_results.xlsx")  
    cnx.close()


def get_today():
    nowdate = str(datetime.datetime.now().strftime("%d-%m-%Y"))
    ads=[]
    cnx = sqlite3.connect('cian.db')
    df = pd.read_sql_query("SELECT * FROM cian_result", cnx)
    df['Date'] = df['Date'].str.split().str[0]
    for i,j in df.iterrows():
        if j.Date == nowdate:
            ads.append(j)
    cnx.close()            
    return ads
