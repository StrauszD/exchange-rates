import logging
from datetime import datetime
import requests

from entities.rate_entity import Rate
from settings import FIXER_API_KEY


class FixerService:

    def get_usd_rate(self):
        rates = self.__make_request()

        if rates.status_code == 200:
            logging.info('Successfully retrieved rates from Fixer')
            rates_json = rates.json()
            timestamp = rates_json['timestamp']
            mxn = rates_json['rates']['MXN']
            usd = rates_json['rates']['USD']

            return Rate(
                last_updated=datetime.fromtimestamp(timestamp).isoformat(),
                value=round((mxn/usd), 2)
            )

        logging.error('Error while retrieving rates from Fixer')

        return Rate(None, None)

    @staticmethod
    def __make_request():
        uri = f'http://data.fixer.io/api/latest?access_key={FIXER_API_KEY}'

        return requests.request('GET', uri)
