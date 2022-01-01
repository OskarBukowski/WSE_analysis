from fpdf import FPDF
from PIL import Image
from data_preparation import Data
from tkinter_input import Execute
import datetime


def create_title(pdf):
    pdf.set_font('helvetica', 'B', 22)
    pdf.set_draw_color(36, 36, 36)
    pdf.set_fill_color(36, 36, 36)
    pdf.set_text_color(255, 250, 250)
    pdf.set_y(0)
    pdf.set_x(0)
    pdf.cell(max_width, 20, f'Report for company {ticker}', fill=True, align='C')
    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)


def create_report(filename='RAPORT.pdf'):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()

    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    create_title(pdf)

    pdf.image('plots/akcja_wolumen.JPG', 10, 40, max_width - 20, 100)

    pdf.image('plots/akcji_rynkowej.JPG', 10, 160, max_width - 20, 100)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.image('plots/black_colored.png', 0, 0, max_width, 10)
    pdf.image('plots/porownanie.JPG', 10, 20, max_width - 20, 100)
    pdf.image('plots/zyskownosci.JPG', 10, 150, max_width - 20, 100)
    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.image('plots/black_colored.png', 0, 0, max_width, 10)
    pdf.image('plots/rynkowej.JPG', 10, 20, max_width - 20, 75)
    pdf.image('plots/rentownosci.JPG', 10, 110, max_width - 20, 75)
    pdf.image('plots/marza.JPG', 10, 200, max_width - 20, 75)
    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.image('plots/black_colored.png', 0, 0, max_width, 10)
    pdf.image('plots/altman_2.JPG', 10, 20, max_width - 20, 75)
    pdf.image('plots/zadluzenia.JPG', 10, 110, max_width - 20, 75)
    pdf.image('plots/plynnosci.JPG', 10, 200, max_width - 20, 75)
    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.set_y(0)
    pdf.set_x(0)
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_fill_color(36, 36, 36)
    pdf.cell(max_width, 15, 'Statistics', ln=True, align='C', fill=True)

    pdf.image('plots/rozklad.JPG', 65, 20, max_width - 70, 90)

    pdf.set_font('helvetica', 'I', 12)
    pdf.set_text_color(255, 250, 250)

    pdf.set_y(25)
    pdf.cell(50, 10, f'Mean : {data_prep_const.statistics()[2]}', ln=True, align='L')

    pdf.set_y(40)
    pdf.cell(50, 10, f'Standard deviation : {data_prep_const.statistics()[1]}', ln=True, align='L')

    pdf.set_y(55)
    pdf.cell(50, 10, f'Skewness : {data_prep_const.statistics()[3]}', ln=True, align='L')

    pdf.set_y(70)
    pdf.cell(50, 10, f'Kurtosis : {data_prep_const.statistics()[4]}', ln=True, align='L')

    pdf.set_y(85)
    pdf.cell(50, 10, f'Minimum : {data_prep_const.statistics()[6]}', ln=True, align='L')

    pdf.set_y(100)
    pdf.cell(50, 10, f'Maximum : {data_prep_const.statistics()[5]}', ln=True, align='L')

    pdf.image('plots/rolling_volatility.JPG', 5, 115, max_width - 10, 90)

    pdf.set_font('helvetica', 'B', 16)
    pdf.set_y(210)

    pdf.cell(80, 8, 'With the given confidence level 0.01 :', ln=True, align='L')

    pdf.set_font('helvetica', 'I', 14)
    pdf.set_y(230)
    pdf.cell(80, 8, f'Historical Value at Risk : {round((data_prep_const.historicalVAR()), 4)}', ln=True, align='L')

    pdf.set_y(245)
    pdf.cell(80, 8, f'Expected Historical Shortfall : {round((data_prep_const.historicalCVAR()), 4)}', ln=True, align='L')

    pdf.set_y(230)
    pdf.set_x(80)
    pdf.cell(160, 8, f'Max Drawdown : {round((data_prep_const.max_drawdown()), 4)}', ln=True, align='C')

    pdf.set_y(245)
    pdf.set_x(80)
    pdf.cell(160, 8, f'Calmar Ratio : {round((data_prep_const.calmar_ratio()), 4)}', ln=True, align='C')

    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.image('plots/black_colored.png', 0, 287, max_width, 15)

    pdf.set_y(0)
    pdf.set_x(0)
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(255, 250, 250)
    pdf.set_fill_color(36, 36, 36)
    pdf.cell(max_width, 15, 'Risk ratios', ln=True, align='C', fill=True)

    pdf.image('plots/rolling_sharpe.JPG', 10, 20, max_width - 20, 75)

    pdf.image('plots/rolling_sortino.JPG', 10, 110, max_width - 20, 75)

    pdf.image('plots/rolling_modigliani.JPG', 10, 200, max_width - 20, 75)

    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)

    pdf.output(filename)


if __name__ == '__main__':

    print("----", datetime.datetime.now())

    Execute.tkinter_open_window()
    ticker = Execute.user_tkinter_input

    print("----", datetime.datetime.now())

    data_prep_const = Data(ticker)



    max_height = 297
    max_width = 210

    print("--WARN--", datetime.datetime.now())

    import vizualization

    print("-WARN---", datetime.datetime.now())
    print("-ATT---", datetime.datetime.now())

    vizualization.plot_altman(vizualization.Altman().altman_calculation(), 'ALTMAN EM SCORE', 'altman_2.JPG')

    print("-ATT---", datetime.datetime.now())

    vizualization.zadluzenia_plot(vizualization.Path().source(), 'WSKAŹNIKI ZADŁUŻENIA', 'zadluzenia.JPG')
    vizualization.plynnosci_plot(vizualization.Path().source(), 'WSKAŹNIK PŁYNNOŚCI BIEŻĄCEJ', 'plynnosci.JPG')
    vizualization.rynkowej_plot(vizualization.Path().source(), 'WSKAŹNIKI WYCENY PRZEDSIĘBIORSTWA', 'rynkowej.JPG')
    vizualization.rentownosci_plot(vizualization.Path().source(), 'WSKAŹNIKI RENTOWNOŚCI', 'rentownosci.JPG')
    vizualization.marza_plot(vizualization.Path().source(), 'MARŻA ZYSKU ZA SPRZEDAŻY', 'marza.JPG')
    vizualization.rynkowej2_plot(vizualization.Path().source(), 'WSKAŹNIKI WARTOŚCI RYNKOWEJ', 'akcji_rynkowej.JPG')
    vizualization.rzis_plot(vizualization.Path().source(), 'WYNIKI SPRZEDAŻY', 'zyskownosci.JPG')
    vizualization.porownanie_plot(vizualization.Path().source(), 'REAKCJA KURSU AKCJI NA ZMIANY W PRZYCHODACH ZE SPRZEDAŻY', 'porownanie.JPG')
    vizualization.kurs_plot(data_prep_const.market_data_from_stooq(), 'KURS AKCJI', 'akcja_wolumen.JPG')
    vizualization.dist_plot(data_prep_const.market_data_from_stooq(), 'ROZKŁAD STÓP ZWROTU', 'rozklad.JPG')
    vizualization.indicator_plot(data_prep_const.financial_metrics_single()[0], 'VOLATILITY', 'Rolliing volatility', 'rolling_volatility.JPG')
    vizualization.indicator_plot(data_prep_const.financial_metrics_single()[2], 'SHARPE RATIO', 'Rolliing Sharpe Ratio', 'rolling_sharpe.JPG')
    vizualization.indicator_plot(data_prep_const.financial_metrics_single()[3], 'SORTINO RATIO', 'Rolliing Sortino Ratio', 'rolling_sortino.JPG')
    vizualization.indicator_plot(data_prep_const.financial_metrics_with_benchmark()[0], 'MODIGLIANI RATIO', 'Rolliing M2 Ratio', 'rolling_modigliani.JPG')

    vizualization.background('grey_colored.png', (58, 58), "3a3a3a")
    vizualization.background('black_colored.png', (36, 36), "#242424")



    create_report()