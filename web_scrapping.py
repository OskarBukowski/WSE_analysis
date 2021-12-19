import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import warnings
import tkinter_input
import wse_stocks_list_to_update

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class ScrappingData:

    def __init__(self, user_tkinter_input, internal_names_database):
        self.user_tkinter_input = user_tkinter_input
        self.internal_names_database = internal_names_database
        self.urls_dict = dict()
        self.frames_dict = dict()

    def get_financial_data(self):
        """ function gets internal stock name from dictionary with given dict key from user and downloads data for
        appropriate dict value """

        self.internal_ticker = self.internal_names_database[str(self.user_tkinter_input)]

        self.urls_dict = dict(
            rzis_web=[f"https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/{self.internal_ticker},Q",
                      tuple([
                          'Przychody ze sprzedaży',
                          'Zysk ze sprzedaży',
                          'Zysk operacyjny (EBIT)',
                          'Zysk netto akcjonariuszy jednostki dominującej',
                          'EBITDA'
                      ])
                      ],
            bilans_web=[f"https://www.biznesradar.pl/raporty-finansowe-bilans/{self.internal_ticker},Q,0",
                        tuple([
                            'Aktywa trwałe',
                            'Aktywa obrotowe',
                            'Kapitał własny akcjonariuszy jednostki dominującej',
                            'Zobowiązania długoterminowe',
                            'Zobowiązania krótkoterminowe',
                            'Wartość firmy'
                        ])
                        ],
            cash_web=[f"https://www.biznesradar.pl/raporty-finansowe-przeplywy-pieniezne/{self.internal_ticker},Q",
                      tuple([
                          'Przepływy pieniężne z działalności operacyjnej',
                          'Przepływy pieniężne z działalności inwestycyjnej',
                          'CAPEX (niematerialne i rzeczowe)',
                          'Przepływy pieniężne z działalności finansowej',
                          'Dywidenda',
                          'Skup akcji',
                          'Free Cash Flow'
                      ])
                      ],
            rynkowej_web=[f"https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/{self.internal_ticker}",
                          tuple([
                              'Kurs',
                              'Cena / Wartość księgowa',
                              'Cena / Przychody ze sprzedaży',
                              'Cena / Zysk',
                              'EV / Przychody ze sprzedaży',
                              'EV / EBIT',
                              'EV / EBITDA'
                          ])
                          ],
            rentownosci_web=[f"https://www.biznesradar.pl/wskazniki-rentownosci/{self.internal_ticker}",
                             tuple([
                                 'ROE',
                                 'ROA',
                                 'Marża zysku netto',
                                 'Marża zysku ze sprzedaży',
                                 'ROIC'
                             ])
                             ],
            zadluzenia_web=[f"https://www.biznesradar.pl/wskazniki-zadluzenia/{self.internal_ticker}",
                            tuple([
                                'Zadłużenie ogólne',
                                'Zadłużenie kapitału własnego',
                            ])
                            ],
            plynnosci_web=[f"https://www.biznesradar.pl/wskazniki-plynnosci/{self.internal_ticker}",
                           tuple([
                               'Płynność bieżąca'
                           ])
                           ]
            # aktywnosci_web=[f"https://www.biznesradar.pl/wskazniki-aktywnosci/{internal_ticker}"],
            # ryzyko_web=[f"https://www.biznesradar.pl/analiza-portfelowa/{internal_ticker}"]
        )

        # for k, v in self.urls_dict.items():
        #     print(k, str(v[0]))
        return self.urls_dict

    def main(self):
        for k, v in self.get_financial_data().items():
            req = requests.get(str(v[0]))
            soup = bs(req.content, features="lxml")

            table = soup.find_all('table', attrs={'class': 'report-table'})
            df = pd.read_html(str(table))[0]

            df = df.transpose()

            df = df.rename(columns=df.iloc[0])
            df = df.fillna(method='backfill')

            df = df.drop(df.tail(1).index)
            df = df.drop(df.head(1).index)

            df = df[list(v[1])]

            for i in range(len(list(v[1]))):
                df[v[1][i]] = df[v[1][i]].str.split('[rk~%]').str[0].str.replace(" ", '').astype(float)

            df.index = df.index.str.split().str[0]

            self.frames_dict[k] = df

        return self.frames_dict


if __name__ == '__main__':
    tkinter_input.Execute.tkinter_open_window()

    output = ScrappingData(tkinter_input.Execute.input,
                           wse_stocks_list_to_update.CheckInternalStockName().internal_name_scrapping()).main()

    test = output['rentownosci_web']

