import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class ScrappingData:


    def __init__(self, user_tkinter_input, internal_names_database):
        self.user_tkinter_input = user_tkinter_input
        self.internal_names_database = internal_names_database

    def get_financial_data(self):
        """ function gets internal stock name from dictionary with given dict key from user and downloads data for
        appropriate dict value """

        internal_ticker = self.internal_names_database[self.user_tkinter_input]

        urls_dict = dict(
            rzis_web=f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{internal_ticker},Q",
            bilans_web=f"https://www.biznesradar.pl/raporty-finansowe-bilans/{internal_ticker},Q,0",
            cash_web=f"https://www.biznesradar.pl/raporty-finansowe-przeplywy-pieniezne/{internal_ticker},Q",
            rynkowej_web=f"https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/{internal_ticker}",
            rentownosci_web=f"https://www.biznesradar.pl/wskazniki-rentownosci/{internal_ticker}",
            przeplywow_web=f"https://www.biznesradar.pl/wskazniki-przeplywow-pienieznych/{internal_ticker}",
            zadluzenia_web=f"https://www.biznesradar.pl/wskazniki-zadluzenia/{internal_ticker}",
            plynnosci_web=f"https://www.biznesradar.pl/wskazniki-plynnosci/{internal_ticker}",
            aktywnosci_web=f"https://www.biznesradar.pl/wskazniki-aktywnosci/{internal_ticker}",
            ryzyko_web=f"https://www.biznesradar.pl/analiza-portfelowa/{internal_ticker}")


    def main(element, lista):
        req = requests.get(element)

        soup = bs(req.content, features="lxml")

        table = soup.find_all('table', attrs={'class': 'report-table'})
        df = pd.read_html(str(table))[0]

        df = df.transpose()

        df = df.rename(columns=df.iloc[0])
        df = df.fillna(method='backfill')

        df = df.drop(df.tail(1).index, df.head(1).index)

        for i in range(len(list(lista))):
            df[lista[i]] = df[lista[i]].str.split('[rk~%]').str[0].str.replace(" ", '').astype(float)

        df.index = df.index.str.split().str[0]

        return df


rzis_elements = tuple(
    'Przychody ze sprzedaży',
    'Zysk ze sprzedaży',
    'Zysk operacyjny (EBIT)',
    'Zysk netto akcjonariuszy jednostki dominującej',
    'EBITDA')

rzis = main(rzis_web, rzis_list)

bilans_elements = tuple('Aktywa trwałe',
               'Aktywa obrotowe',
               'Kapitał własny akcjonariuszy jednostki dominującej',
               'Zobowiązania długoterminowe',
               'Zobowiązania krótkoterminowe',
               'Wartość firmy')

bilans = main(bilans_web, bilans_list)

cash_elements = tuple(
    'Przepływy pieniężne z działalności operacyjnej',
    'Przepływy pieniężne z działalności inwestycyjnej',
    'CAPEX (niematerialne i rzeczowe)',
    'Przepływy pieniężne z działalności finansowej',
    'Dywidenda',
    'Skup akcji',
    'Free Cash Flow'
)

cash = main(cash_web, cash_list)

rynkowej_elements = tuple(
    'Kurs',
    'Cena / Wartość księgowa',
    'Cena / Przychody ze sprzedaży',
    'Cena / Zysk',
    'EV / Przychody ze sprzedaży',
    'EV / EBIT',
    'EV / EBITDA'
)

rynkowej = main(rynkowej_web, rynkowej_list)

rentownosci_elements = tuple(
    'ROE',
    'ROA',
    'Marża zysku netto',
    'Marża zysku ze sprzedaży',
    'ROIC'
)

rentownosci = main(rentownosci_web, rentownosci_list)

zadluzenia_elements = tuple(
    'Zadłużenie ogólne',
    'Zadłużenie kapitału własnego',
)

zadluzenia = main(zadluzenia_web, zadluzenia_list)

plynnosci_elements = 'Płynność bieżąca'

plynnosci = main(plynnosci_web, plynnosci_list)
