import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import warnings
import tkinter_input
import wse_stocks_list_to_update

url = 'https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/KINO-POLSKA-TV,Q'

rzis_list = ['Przychody ze sprzedaży',
          'Zysk ze sprzedaży',
          'Zysk operacyjny (EBIT)',
          'Zysk netto akcjonariuszy jednostki dominującej',
          'EBITDA']

req = requests.get(url)
soup = bs(req.content, features="lxml")

table = soup.find_all('table', attrs={'class': 'report-table'})
df = pd.read_html(str(table))[0]
df = df.transpose()

df = df.rename(columns=df.iloc[0])
df = df.fillna(method='backfill')

df = df.drop(df.tail(1).index)
df = df.drop(df.head(1).index)

for i in range(len(list(rzis_list))):
    df[rzis_list[i]] = df[rzis_list[i]].str.split('[rk~%]').str[0].str.replace(" ", '').astype(float)

df.index = df.index.str.split().str[0]

print(df)