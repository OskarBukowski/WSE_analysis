from fpdf import FPDF
from PIL import Image
import numpy as np
import data_preparation
import web_scrapping
import tkinter_input
import wse_stocks_list_to_update

tkinter_input.Execute.tkinter_open_window()

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
img.save('grey_colored.png')

img = Image.new('RGB', (36, 36), "#242424")
img.save('black_colored.png')


def create_title(pdf):
    pdf.set_font('helvetica', 'B', 22)
    pdf.set_draw_color(36, 36, 36)
    pdf.set_fill_color(36, 36, 36)
    pdf.set_text_color(255, 250, 250)
    pdf.set_y(0)
    pdf.set_x(0)
    pdf.cell(max_width, 20, f'Report for company {ticker}', fill=True, align='C')
    pdf.image('black_colored.png', 0, 287, max_width, 10)


def create_report(filename='RAPORT.pdf'):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()

    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    create_title(pdf)

    pdf.image(name_1, 10, 40, max_width - 20, 100)

    pdf.image(name_2, 10, 160, max_width - 20, 100)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.image('plots/black_colored.png', 0, 0, max_width, 10)
    pdf.image(name_3, 10, 20, max_width - 20, 100)
    pdf.image(name_4, 10, 150, max_width - 20, 100)
    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.image('plots/black_colored.png', 0, 0, max_width, 10)
    pdf.image(name_5, 10, 20, max_width - 20, 75)
    pdf.image(name_6, 10, 110, max_width - 20, 75)
    pdf.image(name_7, 10, 200, max_width - 20, 75)
    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.image('plots/black_colored.png', 0, 0, max_width, 10)
    pdf.image(name_8, 10, 20, max_width - 20, 75)
    pdf.image(name_9, 10, 110, max_width - 20, 75)
    pdf.image(name_10, 10, 200, max_width - 20, 75)
    pdf.image('plots/black_colored.png', 0, 287, max_width, 10)

    pdf.add_page()
    pdf.image('plots/grey_colored.png', x=0, y=0, w=210, h=297, type='', link='')

    pdf.set_y(0)
    pdf.set_x(0)
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_fill_color(36, 36, 36)
    pdf.cell(max_width, 15, 'Statistics', ln=True, align='C', fill=True)

    pdf.image(name_11, 65, 20, max_width - 70, 90)

    pdf.set_font('helvetica', 'I', 12)
    pdf.set_text_color(255, 250, 250)

    pdf.set_y(25)
    pdf.cell(50, 10, f'Mean : {mean}', ln=True, align='L')

    pdf.set_y(40)
    pdf.cell(50, 10, f'Standard deviation : {annualized_std}', ln=True, align='L')

    pdf.set_y(55)
    pdf.cell(50, 10, f'Skewness : {skewness}', ln=True, align='L')

    pdf.set_y(70)
    pdf.cell(50, 10, f'Kurtosis : {kurtosis}', ln=True, align='L')

    pdf.set_y(85)
    pdf.cell(50, 10, f'Minimum : {min_value}', ln=True, align='L')

    pdf.set_y(100)
    pdf.cell(50, 10, f'Maximum : {max_value}', ln=True, align='L')

    pdf.image(name_12, 5, 115, max_width - 10, 90)

    pdf.set_font('helvetica', 'B', 16)
    pdf.set_y(210)

    pdf.cell(80, 8, 'With the given confidence level 0.01 :', ln=True, align='L')

    pdf.set_font('helvetica', 'I', 14)
    pdf.set_y(230)
    pdf.cell(80, 8, f'Historical Value at Risk : {hist_var}', ln=True, align='L')

    pdf.set_y(245)
    pdf.cell(80, 8, f'Expected Historical Shortfall : {hist_cvar}', ln=True, align='L')

    pdf.set_y(230)
    pdf.set_x(80)
    pdf.cell(160, 8, f'Max Drawdown : {drawdown}', ln=True, align='C')

    pdf.set_y(245)
    pdf.set_x(80)
    pdf.cell(160, 8, f'Calmar Ratio : {calmar}', ln=True, align='C')

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

    pdf.image(name_13, 10, 20, max_width - 20, 75)

    pdf.image(name_14, 10, 110, max_width - 20, 75)

    pdf.image(name_15, 10, 200, max_width - 20, 75)

    pdf.image('black_colored.png', 0, 287, max_width, 10)

    pdf.output(filename)


if __name__ == '__main__':
    tkinter_input.Execute.tkinter_open_window()


    ticker = tkinter_input.Execute.user_tkinter_input

    log_returns, annualized_std, mean, skewness, kurtosis, max_value, \
    min_value = data_preparation.Data(ticker).statistics()



    drawdown = round((data_preparation.Data(ticker)
                      .max_drawdown(data_preparation.Data(ticker).financial_metrics_with_benchmark()[1] * 100)), 4)

    calmar = round((np.exp(log_returns.mean() * 252) / abs(
        data_preparation.Data.max_drawdown(data_preparation.Data(ticker).financial_metrics_with_benchmark()[0]))), 4)

    hist_var = round((data_preparation.Data(ticker).historicalVAR(log_returns, data_preparation.Data().ALPHA)), 4)
    hist_cvar = round((data_preparation.Data(ticker).historicalCVAR(log_returns, data_preparation.Data().ALPHA)), 4)

    create_report()
