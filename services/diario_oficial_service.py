import logging
import traceback
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from entities.rate_entity import Rate


class DiarioOficialService:

    def get_usd_rate(self):

        try:
            soup = BeautifulSoup(self.__make_request().content, 'html.parser')
            rates_first_row = soup.find_all('tr', class_='renglonNon')[0]

            date_column = str(rates_first_row.find_all('td')[0])
            date = date_column.replace('<td align=\"left\" style=\"padding-top:5px;padding-bottom:5px;\">',
                                       '').replace('</td>', '').strip()

            value_column = str(rates_first_row.find_all('td')[1])
            value_column_fallback = str(rates_first_row.find_all('td')[3])
            value = self.__get_value(value_column, value_column_fallback)

            return Rate(
                last_updated=datetime.strptime(date, '%d/%m/%Y').isoformat(),
                value=round(float(value), 2)
            )
        except Exception as error:
            logging.error(f'Error while parsing rates from Diaro Oficial scrapper {str(error)}')
            logging.error(traceback.format_exc())

            return Rate(None, None)

    @staticmethod
    def __make_request():
        uri = 'https://www.banxico.org.mx/tipcamb/tipCamMIAction.do'

        return requests.request('GET', uri)

    @staticmethod
    def __get_value(value, fallback):
        if 'N/E' in value:
            return fallback.replace('<td align=\"right\">', '').replace('</td>', '')

        return value.replace('<td align=\"right\">', '').replace('</td>', '')
