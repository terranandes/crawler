#! ../.venv/bin/python3
import sys
import subprocess
#gathering process to complete data

help_msg ='\
Usage: run_all.py [start_year] [end_year]\n\
For example:\n\
run_all.py 2010 2026\
'


start_year_in = 2010
end_year_in   = 2026

if (len(sys.argv) > 1 and sys.argv[1] == '-h') or len(sys.argv) > 3:
    print(help_msg)
    exit()

if len(sys.argv) == 2:
    try:
        start_year_in = int(sys.argv[1])
    except:
        print("Input start_year is not a valid integer!")

if len(sys.argv) == 3:
    try:
        end_year_in = int(sys.argv[2])
    except:
        print("Input end_year is not a valid integer!")

#Async gathering data
subprocess.run(['python3', 'main_async_httpx.py', f'{start_year_in}', f'{end_year_in}'])

subprocess.run(f'rm -f                stock_list_s{start_year_in}e{end_year_in}_unfiltered.csv', shell=True)
subprocess.run(f'cp -f stock_list.csv stock_list_s{start_year_in}e{end_year_in}_unfiltered.csv', shell=True)

#Filtering data
subprocess.run(['python3', 'pandas_stock.py', f'{end_year_in}'])

#Predicting step to next

