import requests
from bs4 import BeautifulSoup as bs
import re
import time



class CheckInternalStockName:
    URL = 'https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/akcje_gpw,Q,IncomeRevenues,0,1'

    def __int__(self):
        pass

    def time(self):
        def counter(*args):
            start = time.time()
            val = self(*args)
            print(f"Execution time {self.__name__}: { time.time() - start}")
            return val

        return counter



    @staticmethod
    @time
    def internal_name_scrapping():
        """ function scrapping data of tickers and internal url addresses of biznesradar.pl website """

        req = requests.get(CheckInternalStockName.URL)
        soup = bs(req.content, features="lxml")
        table = soup.find('table', attrs={'class': 'qTableFull'})
        biznesradar_internal_names = {}

        for row in table.find_all("a"):
            """ loop excludes the rows from table that are markdowns"""

            url_stock_name = row['href'].split('/')[2].split(',')[0]
            ticker = row.get_text().split(' ')[0]

            if re.match("[A-Z][A-Z][A-Z]", str(ticker)):
                if url_stock_name == 'akcje_gpw':
                    continue
                else:
                    biznesradar_internal_names[ticker] = url_stock_name

        return biznesradar_internal_names


# if __name__ == '__main__':
#     print(CheckInternalStockName().internal_name_scrapping())
