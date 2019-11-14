from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
from unidecode import unidecode
import os


def round_if_number(number, n):
    try: return round(float(number), n)
    except ValueError: return number


def main():
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(chrome_options=chrome_options)

    url = 'https://www.hidrografico.pt/m.boias'

    driver.get(url)
    boia_dropdown = driver.find_element_by_id('dropdown')
    boia_dropdown_options = [x.text for x in boia_dropdown.find_elements_by_tag_name('option')]

    per_dropdown = driver.find_element_by_id('per')
    per_dropdown.click()
    select = Select(per_dropdown)
    select.select_by_visible_text('Últimas 48 horas')

    for boia_opt in boia_dropdown_options:
        boia_dropdown.click()
        select = Select(boia_dropdown)
        select.select_by_visible_text(boia_opt)
        par_dropdown = driver.find_element_by_id('par')
        par_dropdown_options = [x.text for x in par_dropdown.find_elements_by_tag_name('option')]

        df_final = None
        for par_opt in par_dropdown_options:
            par_dropdown.click()
            select = Select(par_dropdown)
            select.select_by_visible_text(par_opt)
            time.sleep(2)
            data = driver.find_element_by_id('showData')
            aux = []

            rows = data.find_elements_by_tag_name('tr')
            header = rows.pop(0)
            header = [c.text for c in header.find_elements_by_tag_name('th')]
            for row in rows:
                aux.append([round_if_number(c.text, 1) for c in row.find_elements_by_tag_name('td')])
            
            df = pd.DataFrame.from_records(aux, columns=header)
            df = df.set_index(header[0])
            if df_final is None:
                df_final = df
            else:
                df_final = df_final.join(df)
        output_name = unidecode(boia_opt).replace(' ','_')
        output_location = './output/' + output_name + '/'
        if os.path.isdir(output_location) is False:
            os.makedirs(output_location)
        output_location = output_location + output_name + '.csv'
        df_final.to_csv(output_location, sep=',')


if __name__ == '__main__':
    print('Working...')
    main()
    print('Finished.')
