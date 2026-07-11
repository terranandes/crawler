#! ../.venv/bin/python3
import sys
import subprocess
import csv
import json
import os
#recrawl the codes in recrawl_codes.txt and merge them into the unfiltered CSV

help_msg ='\
Usage: uv run run_all_recrawl.py [start_year] [end_year]\n\
For example:\n\
uv run run_all_recrawl.py 2006 2026\n\
Crawls only the codes in recrawl_codes.txt, merges successful rows into\n\
stock_list_s{start_year}e{end_year}_unfiltered.csv (searched in cwd then ./output),\n\
then reruns pandas_stock.py there\
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
        start_year_in = int(sys.argv[1])
    except:
        print("Input start_year is not a valid integer!")
    try:
        end_year_in = int(sys.argv[2])
    except:
        print("Input end_year is not a valid integer!")

#Locate the unfiltered CSV before crawling, so a wrong cwd fails fast
fn_unfiltered = f'stock_list_s{start_year_in}e{end_year_in}_unfiltered.csv'
csv_dir = None
for candidate in ['.', 'output']:
    if os.path.isfile(os.path.join(candidate, fn_unfiltered)):
        csv_dir = candidate
        break
if csv_dir is None:
    print(f'{fn_unfiltered} not found in ./ or ./output, run run_all.py first')
    exit()
fn_unfiltered = os.path.join(csv_dir, fn_unfiltered)

#Async gathering data for the recrawl codes only
subprocess.run(['python3', 'main_async_httpx_recrawl.py', f'{start_year_in}', f'{end_year_in}'])

#Merge successful recrawl rows into the unfiltered CSV, matching by stock id
with open('stock_list_recrawl.json', 'r', encoding='utf-8') as jsonFile :
    sd_recrawl = json.load(jsonFile)
successful = {}
for row in sd_recrawl[1:] :
    if any(v is not None for v in row[3:]) :
        successful[row[0]] = ['' if v is None else v for v in row]

with open(fn_unfiltered, 'r', newline='', encoding='utf-8') as csvFile :
    stock_rows = list(csv.reader(csvFile))
if stock_rows[0] != sd_recrawl[0] :
    print('Header mismatch between stock_list_recrawl.json and unfiltered CSV, abort merge')
    exit()
merged = 0
for i, row in enumerate(stock_rows) :
    if row[0] in successful :
        new_row = successful.pop(row[0])
        #keep the already known name if the recrawl name query came back empty
        if not new_row[1] and row[1] :
            new_row[1] = row[1]
            new_row[2] = row[2]
        stock_rows[i] = new_row
        merged += 1
with open(fn_unfiltered, 'w', newline='', encoding='utf-8') as csvFile :
    csvWriter = csv.writer(csvFile)
    for row in stock_rows :
        csvWriter.writerow(row)
print(f'Merged {merged} recrawled stocks into {fn_unfiltered}', flush=True)
if successful :
    print(f'Codes not present in the CSV, skipped: {sorted(successful)}', flush=True)
#Keep only the still-empty codes in recrawl_codes.txt for the next run
still_empty = [row[0] for row in sd_recrawl[1:] if all(v is None for v in row[3:])]
with open('recrawl_codes.txt', 'w', encoding='utf-8') as recrawlFile :
    for code in still_empty :
        recrawlFile.write(code + '\n')
print(f'{len(still_empty)} codes still empty, kept in recrawl_codes.txt: {still_empty}', flush=True)

#Filtering data
subprocess.run(['python3', '../pandas_stock.py' if csv_dir == 'output' else 'pandas_stock.py',
                f'{start_year_in}', f'{end_year_in}'], cwd=csv_dir)
