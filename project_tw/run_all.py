#! /root/miniconda3/bin/python3
import subprocess
#gathering process to complete data

#Async gathering data
subprocess.run(['python3', 'main_async_httpx.py'])

subprocess.run('cp -rf stock_list.csv stock_list_s2006e2025_unfiltered.csv', shell=True)

#Filtering data
subprocess.run(['python3', 'pandas_stock.py'])

#Predicting step to next

