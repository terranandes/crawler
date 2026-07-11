#! ../.venv/bin/python3
import sys
import subprocess
import csv
#gathering process to complete data

help_msg ='\
Usage: uv run run_all.py [start_year] [end_year]\n\
For example:\n\
uv run run_all.py 2006 2026\
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

#Async gathering data
crawl = subprocess.run(['python3', 'main_async_httpx.py', f'{start_year_in}', f'{end_year_in}'])
if crawl.returncode != 0 :
    print(f'main_async_httpx.py failed (returncode {crawl.returncode}), abort', flush=True)
    sys.exit(crawl.returncode)

subprocess.run(f'rm -f                stock_list_s{start_year_in}e{end_year_in}_unfiltered.csv', shell=True)
subprocess.run(f'cp -f stock_list.csv stock_list_s{start_year_in}e{end_year_in}_unfiltered.csv', shell=True)

print(f'Complete stock_list_s{start_year_in}e{end_year_in}_unfiltered.csv')

#Extract recrawl candidates into recrawl_codes.txt, ready for a later
#main_async_httpx_recrawl.py pass (e.g. after a server outage):
#rows with no data at all, or with a bao hole after the first non-empty bao
#(legit later-listed stocks only have empty leading ranges, never mid-holes)
def needs_recrawl (row, bao_idx) :
    baos = [row[i] for i in bao_idx]
    first = next((k for k, v in enumerate(baos) if v), None)
    return first is None or '' in baos[first:]

fn_recrawl = 'recrawl_codes.txt'
with open(f'stock_list_s{start_year_in}e{end_year_in}_unfiltered.csv', newline='', encoding='utf-8') as csvFile :
    stock_rows = list(csv.reader(csvFile))
bao_idx = [i for i, cl in enumerate(stock_rows[0]) if cl.endswith('bao')]
empty_codes = [row[0] for row in stock_rows[1:] if needs_recrawl(row, bao_idx)]
with open(fn_recrawl, 'w', encoding='utf-8') as recrawlFile :
    for code in empty_codes :
        recrawlFile.write(code + '\n')
print(f'{len(empty_codes)} recrawl candidates written to {fn_recrawl}')

#Filtering data
subprocess.run(['python3', 'pandas_stock.py', f'{start_year_in}', f'{end_year_in}'])

#Predicting step to next

