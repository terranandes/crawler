import requests as reqs
import json
import csv
import re
import time
import getopt
from datetime import datetime as dt
from bs4 import BeautifulSoup as soup
import bar_chart_race as bcr
import pandas as pd
import getopt
import subprocess
#import multiprocessing
#import threading
import asyncio
import httpx
#import scrapy
#import requests_html
#import plotly
#import scipy
#scikit-learn
#import matplotlib.pyplot as plt
#import numpy as np


#def print_hi(name):
#    print(f'Hi, {name}')  # Print template

#TBD
class ROICrawler:
    pass

def upt_para(para, st, sy, ey) :
    para_dup = dict(para);
    para_dup['stkCode'] = st
    para_dup['startYear'] = sy
    para_dup['endYear'] = ey
    return para_dup

async def get_stock_info_year(i, sy, ey, para_exep, st):
    #global client
    #print('start get_stock_info_year', i, sy, ey, st)
    para_qry = upt_para(para_exep, st, sy, ey)
    retry = True
    while retry:
        try:
            async with httpx.AsyncClient() as aclient:
            #async with client as aclient:
                resp_exep = await aclient.post(url_exep, json=para_qry)
                #resp_exep = reqs.post(url_exep, json=para_qry)
                #print(resp_exep)
                #print(resp_exep.json())
                resp_exep.raise_for_status()  # REVISIT, need redo if received "Bad request'
                retry = False
        except Exception as e:
            print(e, url_exep, para_qry, 'Hello info?')
            print(f'Well, let\'s take a rest: {retry_interval}s')
            time.sleep(retry_interval)

    sd_resp = json.loads(resp_exep.text)  # stock_dict response
    if 'buyAtOpening' in sd_resp:
        bao = float(sd_resp['buyAtOpening']['yroi'].replace(' %', ''))
    else:
        bao = 0
    if 'buyAtHighest' in sd_resp:
        bah = float(sd_resp['buyAtHighest']['yroi'].replace(' %', ''))
    else:
        bah = 0
    if 'buyAtLowest' in sd_resp:
        bal = float(sd_resp['buyAtLowest']['yroi'].replace(' %', ''))
    else:
        bal = 0
    if 'n' in sd_resp:
        yrs = sd_resp['n']
    else:
        yrs = 0
    #print('end get_stock_info_year', i, sy, ey, st)
    return [bao, bah, bal, yrs]

def get_stock_id_name(para_exep, st):
    #global client
    #print('start get_stock_id_name', st)
    para_qry = upt_para(para_exep, st, 2006, 2020)
    retry = True
    while retry:
        try:
            resp_exep = reqs.post(url_exep, json=para_qry)
            #async with httpx.AsyncClient(limits=limits) as aclient:
            #async with client as aclient:
                #resp_exep = await aclient.post(url_exep, json=para_qry)
                #print(resp_exep)
                #print(resp_exep.json())
            resp_exep.raise_for_status()  # REVISIT, need redo if received "Bad request'
            retry = False
        except Exception as e:
            print(e, url_exep, para_qry, 'Hello id?')
            print(f'Well, let\'s take a rest: {retry_interval}s')
            time.sleep(retry_interval)

    sd_resp = json.loads(resp_exep.text)  # stock_dict response
    if 'stkName' in sd_resp:
        stn = sd_resp['stkName']
        id_name = st + '-' + stn
    else:
        stn = None
        id_name = st
    #print('end get_stock_id_name', st)
    return [st, stn, id_name]

async def get_stock_info(i, para_exep, st) :
    #print('start get_stock_info', st)
    tasks = []
    result = []
    #task_get_stock_id_name = asyncio.create_task(get_stock_id_name(para_exep, st))
    result.extend(get_stock_id_name(para_exep, st))
    for sy in range(2006, start_year_ub):  # 2006~2020
        for ey in range(2007, end_year_ub):  # 2007~2021
            if sy < ey :
                tasks.append(get_stock_info_year(i, sy, ey, para_exep, st))
    offset = 0
    size = len(tasks)
    while True:
        if offset > size:
            break
        result_chunk = await asyncio.gather(*tasks[offset:offset+info_chunk])
        result.extend(result_chunk)
        offset += info_chunk
    #result = await asyncio.gather(task_get_stock_id_name, *tasks)
    #result.extend(result_chunk)
    #print('end get_stock_info', st)
    return result

def get_stock_header():
    #print('start get_stock_header')
    stock_header = ['id', 'name', 'id_name']
    for sy in range(2006, start_year_ub):  # 2006~2020
        for ey in range(2007, end_year_ub):  # 2007~2021
            if sy < ey :
                stock_header.append('s' + str(sy) + 'e' + str(ey) + 'bao')
                stock_header.append('s' + str(sy) + 'e' + str(ey) + 'bah')
                stock_header.append('s' + str(sy) + 'e' + str(ey) + 'bal')
                stock_header.append('s' + str(sy) + 'e' + str(ey) + 'yrs')
    #print('end get_stock_header')
    return stock_header

def flatten (lol) :
    for item in lol:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

async def main(stock_list, para_exep):
    #global client
    #print('start asyncio.run')
    #result = await asyncio.gather(*[get_stock_info(i,para_exep, stock) for i, stock in enumerate(stock_100, start=0)])
    result = await asyncio.gather(*[get_stock_info(i,para_exep, stock) for i, stock in enumerate(stock_list, start=0)])
    #await client.aclose()
    #result = await asyncio.gather(group)
    #print('Stock Header:' ,stock_header) #right result
    #print('Main result1:' ,result)
    result_final = []
    #result_final.append(stock_header)
    for stock_entry in result:
        stock_flt = list(flatten(stock_entry))
        result_final.append(stock_flt)
    print('Fianl result:', result_final)
    return result_final

def get_supportred_stock (url) :
    resp = reqs.get(url)
    resp.raise_for_status()
    #print(resp_orig.text) #type : string
    page = resp.text
    soup_page = soup(page, "html.parser")
    #print(soup_orig.prettify())
    for script in soup_page.find_all('script') :
     if re.search("g_stocks", str(script.string)):
        g_stocks = str(script.string)
        break
    #print (g_stocks)
    stock_list = re.findall(':"(.+)",' ,g_stocks)
    print(stock_list)
    return stock_list

if __name__ == '__main__':
    starttime = dt.now()
    print(starttime)
    #initialize variable
    #User modifiable CFG, To be configured by getopt module
    #max_live_connect_httpx = 1 #None #5, max 10
    #max_connect_httpx = 1 #None #10, max 100
    stock_chunk = 1
    info_chunk = 60
    start_year_ub = 2021
    end_year_ub = 2022
    retry_interval = 1

    #limits = httpx.Limits(max_keepalive_connections=max_live_connect_httpx, max_connections=max_connect_httpx)
    #client = httpx.AsyncClient(limits=limits)
    url_orig = "https://www.moneycome.in/tool/compound_interest?stkCode=6533"
    url_exep = "https://www.moneycome.in/piggy/s/ci/calcStock"
    para_exep = { "stkCode":"6533",
                "principle":1000000,
                "invAmtPerPeriod":60000,
                "startYear":2006,
                "endYear":2021,
                "isDividendReinvestment":True,
                "isCrashInvestment":False,
                "crashThreshold":0.3,
                "invAmtForCrash":60000}

    #Get supported stock list
    stock_list = get_supportred_stock(url_orig)
    #print(stock_list)

    #Get expansion rate of each stock
    fn_json = 'stock_list.json'
    #try:
    #  with open(fn_json, 'r', encoding='utf-8') as jsonFile :
    #    sd_l = json.load(jsonFile)
    #except Exception :
    #  sd_l = []

    sd_l = []
    stock_header = get_stock_header()
    sd_l.append(stock_header) #get csv first row
    print('Stock Header:' ,stock_header) #right result
    offset = 0
    size = len(stock_list)
    print('stock number:', size)
    while True:
        if offset > size:
            break
        sd_chunk = asyncio.run(main(stock_list[offset:offset+stock_chunk], para_exep))
        sd_l.extend(sd_chunk)
        offset += stock_chunk

    #sd_l = asyncio.run(main(stock_list, para_exep))

    print(sd_l)

    # output JSON and CSV File
    # JSON & DICT format
    # [[6533,                #id
    #  晶心科,                #name
    #  6533-晶心科            #id_name
    #  26.7,                 #s2006e2007
    #  .................,
    #  xxxx,                 #s2019e2020
    #  yy.y,
    #  xx.y],
    #  [...],                #another stock info
    #  ...
    #  [...]
    # ]
    with open(fn_json, 'w', encoding='utf-8') as jsonFile :
      json.dump(sd_l, jsonFile, indent=2, ensure_ascii=False)

    #CSV format
    #id name s2006e2007 s2006e2008 ... s2006e2020 s2007e2008 ...s2007e2020 .. s2019e2020
    fn_csv = 'stock_list.csv'
    with open(fn_csv, 'w', newline = '', encoding='utf-8') as csvFile :
      csvWriter = csv.writer(csvFile)
      for row in sd_l :
        csvWriter.writerow(row)
      
    #Second Step
    #Data Analysis using Pandas
    #Todo begin
    #Todo end
    #Final Step
    #Animation for it
    #Todo Begin
    #bar_chart_race
    #Todo End

print('                  _            ')
print('                /`o\__         ')
print('         ,_     \ _.==\'        ')
print('        `) `----`~~\           ')
print('      -~ \  \'~-.   / ~-        ')
print('       ~- `~-====-\ ~_ ~-      ')
print('      ~ - ~ ~- ~ - ~ -         ')

endtime = dt.now()
print(endtime)
print('Time Spend:')
print(endtime-starttime)