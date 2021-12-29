import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
import pandas_datareader.data as web
import data_preparation
import web_scrapping
import tkinter_input
import wse_stocks_list_to_update


tkinter_input.Execute.tkinter_open_window()



class Path:
    def __init__(self):
        self.fin_source = None

    @staticmethod
    def connection(fin_data):
        frame = web_scrapping.ScrappingData(tkinter_input.Execute.user_tkinter_input,
                                            wse_stocks_list_to_update.CheckInternalStockName().
                                            check_ticker()).main()[fin_data]

        return frame

    def source(self):
        fin_source = dict(
            bilans=self.connection('bilans_web'),
            rzis=self.connection('rzis_web'),
            cash=self.connection('cash_web'),
            rynkowej=self.connection('rynkowej_web'),
            rentownosci=self.connection('rentownosci_web'),
            zadluzenia=self.connection('zadluzenia_web'),
            plynnosci=self.connection('plynnosci_web')
        )

        return fin_source




class Altman:
    def __init__(self):
        self.altman = pd.DataFrame()

    def altman_calculation(self):
        altman_calc = Path().source()

        self.altman['one'] = 6.65 * ((altman_calc['bilans']['Aktywa obrotowe'] -
                                      altman_calc['bilans']['Zobowiązania krótkoterminowe']) /
                                     (altman_calc['bilans']['Aktywa trwałe'] +
                                      altman_calc['bilans']['Aktywa obrotowe']))

        self.altman['two'] = 3.26 * ((altman_calc['rzis']['Zysk netto akcjonariuszy jednostki dominującej'] -
                                      altman_calc['cash']['Dywidenda']) /
                                     (altman_calc['bilans']['Aktywa trwałe'] +
                                      altman_calc['bilans']['Aktywa obrotowe']))

        self.altman['three'] = 6.72 * (altman_calc['rzis']['Zysk operacyjny (EBIT)'] /
                                       (altman_calc['bilans']['Aktywa trwałe'] +
                                        altman_calc['bilans']['Aktywa obrotowe']))

        self.altman['four'] = 1.05 * (altman_calc['bilans']['Kapitał własny akcjonariuszy jednostki dominującej'] /
                                      (altman_calc['bilans']['Zobowiązania krótkoterminowe'] +
                                       altman_calc['bilans']['Zobowiązania długoterminowe']))

        self.altman = self.altman.fillna(method='backfill')

        self.altman['em_score'] = self.altman['one'] + self.altman['two'] + self.altman['three'] + self.altman[
            'four'] + 3.25

        return self.altman


def plot_altman(data, title):
    xticks_alt = data.index[::4]

    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(18, 8))
    plt.title(title, fontsize=20)
    plt.plot(data['em_score'], color='r', linestyle='-', linewidth=3)
    plt.grid(axis='x', alpha=0.5)
    plt.xticks(xticks_alt, fontsize=13)
    plt.yticks(fontsize=14)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()

    return plt.savefig('plots/altman_2.JPG')


plot_altman(Altman().altman_calculation(), 'ALTMAN EM SCORE')


def zadluzenia_plot(data, title, file_name):
    xticks_zad = data['zadluzenia'].index[::4]
    yticks = np.arange(0.0, 2.5, 0.25)

    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(22, 8))
    plt.title(title, fontsize=20)
    plt.plot(data['zadluzenia']['Zadłużenie kapitału własnego'], color='r', linestyle='-', linewidth=3,
             label='Zadłużenie kapitału własnego')
    plt.plot(data['zadluzenia']['Zadłużenie ogólne'], color='C2', linestyle='-', linewidth=3,
             label='Zadłużenie ogólne')
    plt.grid(axis='y', alpha=0.5)
    plt.xticks(xticks_zad, fontsize=13)
    plt.yticks(yticks, fontsize=14)
    plt.legend(fontsize=14)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()
    plt.savefig(f"plots/{file_name}")


zadluzenia_plot(Path().source(), 'WSKAŹNIKI ZADŁUŻENIA', 'zadluzenia.JPG')



def plynnosci_plot(data, title, file_name):

    xticks_pln = data['plynnosci'].index[::4]

    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(18, 8))
    plt.title(title, fontsize=20)

    plt.plot(data['plynnosci']['Płynność bieżąca'], color='c', linestyle='-', linewidth=3,
             label='Płynność bieżąca')

    plt.plot(data['plynnosci']['Płynność bieżąca'], color='c', linestyle='-', linewidth=3)

    plt.grid(axis='y', alpha=0.5)
    plt.xticks(xticks_pln, fontsize=13)
    plt.yticks(fontsize=14)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()

    return plt.savefig(f'plots/{file_name}')


plynnosci_plot(Path().source(), 'WSKAŹNIK PŁYNNOŚCI BIEŻĄCEJ', 'plynnosci.JPG')


def rynkowej_plot(data, title, file_name):
    xticks_ev = data['rynkowej'].index[::4]

    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(18, 8))
    plt.title(title, fontsize=20)
    plt.plot(data['rynkowej']['EV / EBITDA'], color='c', linestyle='-',
             linewidth=3, label='EV/EBITDA')
    plt.plot(data['rynkowej']['EV / Przychody ze sprzedaży'], color='r', linestyle='-',
             linewidth=3, label='EV/REVENUE')

    plt.grid(axis='y', alpha=0.5)

    plt.xticks(xticks_ev, fontsize=12)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=12)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()

    return plt.savefig(f'plots/{file_name}')


rynkowej_plot(Path().source(), 'WSKAŹNIKI WYCENY PRZEDSIĘBIORSTWA', 'rynkowej.JPG')


def rentownosci_plot(data, title, file_name):
    xticks_rent = data['rentownosci'].index[::4]

    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(18, 8))
    plt.title(title, fontsize=20)
    plt.plot(data['rentownosci']['ROE'], color='c', linestyle='-', linewidth=3, label='ROE')
    plt.plot(data['rentownosci']['ROA'], color='r', linestyle='-', linewidth=3, label='ROA')
    plt.plot(data['rentownosci']['ROIC'], color='m', linestyle='-', linewidth=3, label='ROIC')
    plt.grid(axis='y', alpha=0.5)

    plt.xticks(xticks_rent, fontsize=12)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()

    return plt.savefig(f'plots/{file_name}')


rentownosci_plot(Path().source(), 'WSKAŹNIKI RENTOWNOŚCI', 'rentownosci.JPG')



def marza_plot(data, title, file_name):
    xticks_rent = data['rentownosci'].index[::4]
    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(18, 8))
    plt.title(title, fontsize=20)
    plt.plot(data['rentownosci']['Marża zysku ze sprzedaży'], color='c', linestyle='-', linewidth=3,
             label='Marża zysku ze sprzedaży')
    plt.grid(axis='y', alpha=0.5)

    plt.xticks(xticks_rent, fontsize=12)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()

    return plt.savefig(f'plots/{file_name}')


marza_plot(Path().source(), 'MARŻA ZYSKU ZA SPRZEDAŻY', 'marza.JPG')





def rynkowej2_plot(data, title, file_name):
    xticks_ryn = data['rynkowej'].index[::4]

    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(18, 8))

    plt.title(title, fontsize=20)
    plt.plot(data['rynkowej']['Cena / Zysk'], color='r', linestyle='-', linewidth=3, label='P/E')
    plt.plot(data['rynkowej']['Cena / Wartość księgowa'], color='C2', linestyle='-',
             linewidth=3, label='P/BV')
    plt.plot(data['rynkowej']['Cena / Przychody ze sprzedaży'], color='c', linestyle='-',
             linewidth=3, label='P/REVENUE')
    plt.grid(axis='y', alpha=0.5)

    plt.xticks(xticks_ryn, fontsize=12)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()

    return plt.savefig(f'plots/{file_name}')


rynkowej2_plot(Path().source(), 'WSKAŹNIKI WARTOŚCI RYNKOWEJ', 'akcji_rynkowej.JPG')



def rzis_plot(data, title, file_name):

    xticks_rzis = data['rzis'].index[::4]

    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(18, 8))

    plt.title(title, fontsize=20)
    plt.plot(data['rzis']['Zysk ze sprzedaży'], color='r', linestyle='-',
             linewidth=3, label='Zysk ze sprzedaży')
    plt.plot(data['rzis']['Zysk operacyjny (EBIT)'], color='C2', linestyle='-', linewidth=3, label='EBIT')
    plt.grid(axis='y', alpha=0.5)

    plt.xticks(xticks_rzis, fontsize=12)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()
    plt.savefig('plots/zyskownosci.JPG')

    return plt.savefig(f'plots/{file_name}')


rzis_plot(Path().source(), 'WYNIKI SPRZEDAŻY', 'zyskownosci.JPG')



def porownanie_plot(data, title, file_name):
    porownanie = pd.DataFrame()

    porownanie['Kurs'] = data['rynkowej']['Kurs']
    porownanie['Przychody ze sprzedaży'] = data['rzis']['Przychody ze sprzedaży']

    porownanie = porownanie.loc[porownanie['Kurs'] > 0.0]  # delete first periods because of the often lack of data

    xticks_por = porownanie.index[::4]

    fig, ax1 = plt.subplots()

    fig.set_figheight(8)
    fig.set_figwidth(18)

    plt.title(title, fontsize=20)

    ax1.plot(porownanie['Kurs'], color='r')
    ax1.set_xticks(xticks_por)
    ax1.set_xticklabels(xticks_por)
    ax1.spines['top'].set_visible(False)
    ax1.tick_params(axis='x', labelsize=14)
    ax1.tick_params(axis='y', labelsize=14, labelcolor='r')
    ax1.grid(alpha=0.5)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.plot(porownanie['Przychody ze sprzedaży'], color='C2')
    ax2.set_xticks(xticks_por)
    ax2.set_xticklabels(xticks_por, color='C2')
    ax2.spines['top'].set_visible(False)
    ax2.tick_params(axis='x', labelsize=14)
    ax2.tick_params(axis='y', labelsize=14, labelcolor='C2')
    ax2.grid(alpha=0.0)

    fig.tight_layout()
    plt.show()

    return plt.savefig(f'plots/{file_name}')


porownanie_plot(Path().source(), 'REAKCJA KURSU AKCJI NA ZMIANY W PRZYCHODACH ZE SPRZEDAŻY', 'porownanie.JPG')



def kurs_plot(data, title, file_name):


    asset = data
    asset['Delta'] = asset['Close'].pct_change()

    asset['Date'] = pd.to_datetime(asset.index)
    asset = asset.set_index('Date', drop=True)

    plt.figure(figsize=(18, 8))

    up_fig = plt.subplot2grid((5, 4), (0, 0), rowspan=4, colspan=5)
    up_fig.plot(asset['Close'], color='r', linewidth=3)
    plt.grid(alpha=0.5)
    plt.title(label=title, fontsize=20)
    plt.setp(up_fig.get_xticklabels(), visible=False)

    bottom_fig = plt.subplot2grid((5, 4), (4, 0), rowspan=2, colspan=4, sharex=up_fig)
    bottom_fig.bar(asset.index, asset['Volume'])
    plt.show()

    return plt.savefig(f'plots/{file_name}')


kurs_plot(data_preparation.Data.market_data_from_stooq(), 'KURS AKCJI', 'akcja_wolumen.JPG')


def dist_plot(data, title, file_name):

    asset = data
    asset['Delta'] = asset['Close'].pct_change()

    asset['Date'] = pd.to_datetime(asset.index)
    asset = asset.set_index('Date', drop=True)

    fig = plt.figure(figsize=(14, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    asset['Delta'].hist(bins=50, ax=ax1)
    ax1.set_xlabel('Return', fontsize=14)
    ax1.set_ylabel('Frequency', fontsize=14)
    ax1.set_title(title, fontsize=20)
    ax1.tick_params(axis='x', labelsize=14)
    ax1.tick_params(axis='y', labelsize=14)
    plt.grid(alpha=0.5)
    plt.savefig('plots/rozklad.JPG')
    plt.show()

    return plt.savefig(f'plots/{file_name}')


dist_plot(data_preparation.Data.market_data_from_stooq(), 'ROZKŁAD STÓP ZWROTU', 'rozklad.JPG')


def indicator_plot(data, title, label, file_name):
    plt.style.use('dark_background')
    plt.get_cmap('twilight')

    plt.figure(figsize=(18, 8))

    plt.title(title, fontsize=20)
    plt.plot(data, color='r',
             linestyle='-', linewidth=3, label=label)
    plt.grid(axis='y', alpha=0.5)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(fontsize=14)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.show()

    return plt.savefig(f'plots/{file_name}')


indicator_plot(data_preparation.Data(tkinter_input.Execute.user_tkinter_input).financial_metrics_single()[0],
               'VOLATILITY',
               'Rolliing volatility', 'rolling_volatility.JPG')


indicator_plot(data_preparation.Data(tkinter_input.Execute.user_tkinter_input).financial_metrics_single()[2],
               'SHARPE RATIO',
               'Rolliing Sharpe Ratio', 'rolling_sharpe.JPG')


indicator_plot(data_preparation.Data(tkinter_input.Execute.user_tkinter_input).financial_metrics_single()[3],
               'SORTINO RATIO',
               'Rolliing Sortino Ratio', 'rolling_sortino.JPG')


indicator_plot(data_preparation.Data(tkinter_input.Execute.user_tkinter_input).financial_metrics_with_benchmark()[0],
               'MODIGLIANI RATIO',
               'Rolliing M2 Ratio', 'rolling_modigliani.JPG')
