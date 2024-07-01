import requests
from lxml import html
import pandas as pd
import csv

TARGET_URL = 'https://ru.investing.com/currencies/exchange-rates-table'
HEADER_XPATH = '//*[@id="exchange_rates_1"]/thead/tr'
TABLE_XPATH = '//*[@id="exchange_rates_1"]/tbody/tr'

"""
блок объявления функций
"""

# получаем первую строку заголовка
def get_header_row(header_xpath: str) -> list:
  header = tree.xpath(header_xpath)
  cols = header[0].xpath('th/text()')

  # убираем пустые значения из списка заголовков
  cols = cols[2:]
  cols = [i.strip() for i in cols if i.strip() != '']
  return cols


# получаем значения из таблицы
def get_table_rows(table_xpath: str, header: list) -> list:
  table = tree.xpath(table_xpath)
  currencies = []

  # на этом сайте каждому заголовку соответсвует +2 элемент строки (почему-то)
  for row in table:
    data = {}
    for i in range(0, len(header)):
      data['currency'] = str(row.xpath('.//td/text()')[1].strip())
      data[header[i]] = float(
          row.xpath('.//td/text()')[i + 2].strip().replace(',', '.'))
    currencies.append(data)
  return currencies

"""
блок обработки (основной)
"""
if __name__ == "__main__":
  try:
    req = requests.get(
        url=TARGET_URL,
        headers={
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        })
  except Exception as err:
    print('Smth wrong')
    print(req.status_code, err, sep=' | ')
  
  tree = html.fromstring(req.content)
  header = get_header_row(header_xpath=HEADER_XPATH)
  table_data = get_table_rows(table_xpath=TABLE_XPATH, header=header)
  
  # записываем данные в csv файл
  with open('currency_dependencies.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=table_data[0])
    writer.writeheader()
    writer.writerows(table_data)
  
  # выводим cvs в DataFrame
  print(pd.read_csv('currency_dependencies.csv'))