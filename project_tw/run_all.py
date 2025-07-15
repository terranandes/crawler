#! /root/miniconda3/bin/python3
import sys
import subprocess
#gathering process to complete data

help_msg ='\
Usage: run_all.py [end_year]\n\
For example:\n\
run_all.py 2025\
'

end_year_in = '2025'
if (len(sys.argv) > 1 and sys.argv[1] == '-h') or len(sys.argv) > 2:
    print(help_msg)
    exit()

if len(sys.argv) == 2:
    end_year_in = sys.argv[1]

#Async gathering data
subprocess.run(['python3', 'main_async_httpx.py', end_year_in])

subprocess.run('cp -rf stock_list.csv stock_list_s2006e'+end_year_in+'_unfiltered.csv', shell=True)

#Filtering data
subprocess.run(['python3', 'pandas_stock.py', end_year_in])

#Predicting step to next

