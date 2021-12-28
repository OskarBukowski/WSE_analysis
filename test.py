import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
import pandas_datareader.data as web
import data_preparation
import web_scrapping
import tkinter_input
import wse_stocks_list_to_update

# WYKRESY#####################################################################

tkinter_input.Execute.tkinter_open_window()


# Altman EM-Score   --------------------------

class Path:
    def __init__(self):
        self.fin_source = None

    @staticmethod
    def connection(fin_data):
        frame = web_scrapping.ScrappingData(tkinter_input.Execute.user_tkinter_input,
                                            wse_stocks_list_to_update.CheckInternalStockName().
                                            internal_name_scrapping()).main()[fin_data]

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


xticks_alt = Altman().altman_calculation().index[::4]

plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))
plt.title('ALTMAN EM-SCORE', fontsize=20)
plt.plot(Altman().altman_calculation()['em_score'], color='r', linestyle='-', linewidth=3)
plt.grid(axis='x', alpha=0.5)
plt.xticks(xticks_alt, fontsize=13)
plt.yticks(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/altman_2.JPG')

# Zadłużenie ogółem  |   Zadłużenie kapitału własnego   ------------------

xticks_zad = Path().source()['zadluzenia'].index[::4]
yticks = np.arange(0.0, 2.5, 0.25)

plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(22, 8))
plt.title('WSKAŹNIKI ZADŁUŻENIA', fontsize=20)
plt.plot(Path().source()['zadluzenia']['Zadłużenie kapitału własnego'], color='r', linestyle='-', linewidth=3,
         label='Zadłużenie kapitału własnego')
plt.plot(Path().source()['zadluzenia']['Zadłużenie ogólne'], color='C2', linestyle='-', linewidth=3, label='Zadłużenie ogólne')
plt.grid(axis='y', alpha=0.5)
plt.xticks(xticks_zad, fontsize=13)
plt.yticks(yticks, fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/zadluzenia.JPG')

# Wskaźnik bieżącej płynnosci   -------------------------------------------


xticks_pln = Path().source()['plynnosci'].index[::4]

plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))
plt.title('WSKAŹNIK PŁYNNOŚCI BIEŻĄCEJ', fontsize=20)
plt.plot(Path().source()['plynnosci']['Płynność bieżąca'], color='c', linestyle='-', linewidth=3)
plt.grid(axis='y', alpha=0.5)
plt.xticks(xticks_pln, fontsize=13)
plt.yticks(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/plynnosci.JPG')

# EV/EBITDA,REVENUE  |  Cena akcji -------------------------------------------

xticks_ev = Path().source()['rynkowej'].index[::4]

plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))
plt.title('WSKAŹNIKI WYCENY PRZEDSIĘBIORSTWA', fontsize=20)
plt.plot(Path().source()['rynkowej']['EV / EBITDA'], color='c', linestyle='-', linewidth=3, label='EV/EBITDA')
plt.plot(Path().source()['rynkowej']['EV / Przychody ze sprzedaży'], color='r', linestyle='-', linewidth=3, label='EV/REVENUE')
plt.grid(axis='y', alpha=0.5)

plt.xticks(xticks_ev, fontsize=12)
plt.yticks(fontsize=14)
plt.legend(fontsize=12)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/rynkowej.JPG')

# ROE, ROA, ROS, ROIC, Marża zysku ze sprzedaży   -------------------------


xticks_rent = Path().source()['rentownosci'].index[::4]

# 1


plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))
plt.title('WSKAŹNIKI RENTOWNOŚCI', fontsize=20)
plt.plot(Path().source()['rentownosci']['ROE'], color='c', linestyle='-', linewidth=3, label='ROE')
plt.plot(Path().source()['rentownosci']['ROA'], color='r', linestyle='-', linewidth=3, label='ROA')
plt.plot(Path().source()['rentownosci']['ROIC'], color='m', linestyle='-', linewidth=3, label='ROIC')
plt.grid(axis='y', alpha=0.5)

plt.xticks(xticks_rent, fontsize=12)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/rentownosci.JPG')

# # 2


plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))
plt.title('MARŻA ZYSKU ZA SPRZEDAŻY', fontsize=20)
plt.plot(Path().source()['rentownosci']['Marża zysku ze sprzedaży'], color='c', linestyle='-', linewidth=3,
         label='Marża zysku ze sprzedaży')
plt.grid(axis='y', alpha=0.5)

plt.xticks(xticks_rent, fontsize=12)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/marza.JPG')

# P/E,BV,REVENUE    |  Cena akcji ------------------------------------------

xticks_ryn = Path().source()['rynkowej'].index[::4]

plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))

plt.title('WSKAŹNIKI WARTOŚCI RYNKOWEJ', fontsize=20)
plt.plot(Path().source()['rynkowej']['Cena / Zysk'], color='r', linestyle='-', linewidth=3, label='P/E')
plt.plot(Path().source()['rynkowej']['Cena / Wartość księgowa'], color='C2', linestyle='-', linewidth=3, label='P/BV')
plt.plot(Path().source()['rynkowej']['Cena / Przychody ze sprzedaży'], color='c', linestyle='-', linewidth=3, label='P/REVENUE')
plt.grid(axis='y', alpha=0.5)

plt.xticks(xticks_ryn, fontsize=12)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/akcji_rynkowej.JPG')

# Zysk ze sprzedaży  |  EBIT -------------------------------------------

xticks_rzis = Path().source()['rzis'].index[::4]

plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))

plt.title('WYNIKI SPRZEDAŻY', fontsize=20)
plt.plot(Path().source()['rzis']['Zysk ze sprzedaży'], color='r', linestyle='-', linewidth=3, label='Zysk ze sprzedaży')
plt.plot(Path().source()['rzis']['Zysk operacyjny (EBIT)'], color='C2', linestyle='-', linewidth=3, label='EBIT')
plt.grid(axis='y', alpha=0.5)

plt.xticks(xticks_rzis, fontsize=12)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/zyskownosci.JPG')

# Cena akcji  |  Przychody   ------------------------------------------

porownanie = pd.DataFrame()

porownanie['Kurs'] = Path().source()['rynkowej']['Kurs']
porownanie['Przychody ze sprzedaży'] = Path().source()['rzis']['Przychody ze sprzedaży']

porownanie = porownanie.loc[
    porownanie['Kurs'] > 0.0]  # usuwam okresy początkowe zaburzające dane w czasie gdy akcje nie były w obiegu

xticks_por = porownanie.index[::4]

fig, ax1 = plt.subplots()

fig.set_figheight(8)
fig.set_figwidth(18)

plt.title('REAKCJA KURSU AKCJI NA ZMIANY W PRZYCHODACH ZE SPRZEDAŻY', fontsize=20)

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
plt.savefig('plots/porownanie.JPG')

### STATYSTYKA ###############################################################


asset = web.DataReader(f"{tkinter_input.Execute.user_tkinter_input}.PL", 'stooq')

# print(asset)

asset = asset.drop(columns=['Open', 'High', 'Low'])
asset['Delta'] = asset['Close'].pct_change()

asset['Date'] = pd.to_datetime(asset.index)
asset = asset.set_index('Date', drop=True)

plt.figure(figsize=(18, 8))

up_fig = plt.subplot2grid((5, 4), (0, 0), rowspan=4, colspan=5)
up_fig.plot(asset['Close'], color='r', linewidth=3)
plt.grid(alpha=0.5)
plt.title(label='KURS AKCJI', fontsize=20)
plt.setp(up_fig.get_xticklabels(), visible=False)

bottom_fig = plt.subplot2grid((5, 4), (4, 0), rowspan=2, colspan=4, sharex=up_fig)
bottom_fig.bar(asset.index, asset['Volume'])
plt.show()
plt.savefig('plots/akcja_wolumen.JPG')

# Rozkład stóp zwrotu ----------------------------------------------

fig = plt.figure(figsize=(14, 6))
ax1 = fig.add_subplot(1, 1, 1)
asset['Delta'].hist(bins=50, ax=ax1)
ax1.set_xlabel('Return', fontsize=14)
ax1.set_ylabel('Frequency', fontsize=14)
ax1.set_title('ROZKŁAD STÓP ZWROTU', fontsize=20)
ax1.tick_params(axis='x', labelsize=14)
ax1.tick_params(axis='y', labelsize=14)
plt.grid(alpha=0.5)
plt.savefig('plots/rozklad.JPG')
plt.show()

# ---------------------------------------
plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))

plt.title('VOLATILITY', fontsize=20)
plt.plot(data_preparation.Data(tkinter_input.Execute.user_tkinter_input).financial_metrics_single()[0], color='r',
         linestyle='-', linewidth=3, label='Rolliing volatility')
plt.grid(axis='y', alpha=0.5)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.savefig('plots/rolling_volatility.JPG')
plt.show()
# ----------------------------------------
plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))

plt.title('SHARPE RATIO', fontsize=20)
plt.plot(data_preparation.Data(tkinter_input.Execute.user_tkinter_input).financial_metrics_single()[2],
         color='r',
         linestyle='-',
         linewidth=3,
         label='Rolliing Sharpe Ratio')

plt.grid(axis='y', alpha=0.5)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.savefig('plots/rolling_sharpe.JPG')
plt.show()

# ----------------------------------------
plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))

plt.title('SORTINO RATIO', fontsize=20)
plt.plot(data_preparation.Data(tkinter_input.Execute.user_tkinter_input).financial_metrics_single()[3],
         color='r',
         linestyle='-',
         linewidth=3,
         label='Rolliing Sortino Ratio')

plt.grid(axis='y', alpha=0.5)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.savefig('plots/rolling_sortino.JPG')
plt.show()

# --------------------------------------------------------------------
plt.style.use('dark_background')
plt.get_cmap('twilight')

plt.figure(figsize=(18, 8))

plt.title('MODIGLIANI RATIO', fontsize=20)
plt.plot(data_preparation.Data(tkinter_input.Execute.user_tkinter_input).financial_metrics_with_benchmark()[0],
         color='r',
         linestyle='-',
         linewidth=3,
         label='Rolliing M2 Ratio')

plt.grid(axis='y', alpha=0.5)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.show()
plt.savefig('plots/rolling_modigliani.JPG')

max_height = 297
max_width = 210

name_1 = 'akcja_wolumen.JPG'
name_2 = 'akcji_rynkowej.JPG'
name_3 = 'porownanie.JPG'
name_4 = 'zyskownosci.JPG'
name_5 = 'rynkowej.JPG'
name_6 = 'rentownosci.JPG'
name_7 = 'marza.JPG'
name_8 = 'altman_2.JPG'
name_9 = 'zadluzenia.JPG'
name_10 = 'plynnosci.JPG'
name_11 = 'rozklad.JPG'
name_12 = 'rolling_volatility.JPG'
name_13 = 'rolling_sharpe.JPG'
name_14 = 'rolling_sortino.JPG'
name_15 = 'rolling_modigliani.JPG'
name_16 = 'normality_plot.JPG'

img = Image.new('RGB', (58, 58), "#3a3a3a")
img.save('plots/grey_colored.png')

img = Image.new('RGB', (36, 36), "#242424")
img.save('plots/black_colored.png')
