import traceback
from datetime import datetime
import requests
import logging

from entities.rate_entity import Rate
from settings import BANXICO_API_KEY, BANXICO_SERIES


class BanxicoService:

    def get_usd_rate(self):
        rates = self.__make_request()

        if rates.status_code == 200:
            try:
                logging.info('Successfully retrieved rates from Banxico')
                rates_json = rates.json()
                rate = rates_json['bmx']['series'][0]['datos'][0]
                date = rate['fecha']
                value = rate['dato']

                return Rate(
                    last_updated=datetime.strptime(date, '%d/%m/%Y').isoformat(),
                    value=round(float(value), 2)
                )
            except Exception as error:
                logging.error(f'Error while parsing rates from Banxico {str(error)}')
                logging.error(traceback.format_exc())

                return Rate(None, None)

        logging.error('Error while retrieving rates from Banxico')

        return Rate(None, None)

    @staticmethod
    def __make_request():
        today = datetime.today().strftime('%Y-%m-%d')
        uri = f'https://www.banxico.org.mx/SieAPIRest/service/v1/series/{BANXICO_SERIES}/datos/{today}/{today}?token={BANXICO_API_KEY}'

        return requests.request('GET', uri)
