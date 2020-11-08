from os import getenv

BASE_ROUTE = getenv('BASE_ROUTE', 'api/v1/exchange-rate')
FIXER_API_KEY = getenv('FIXER_API_KEY')
BANXICO_API_KEY = getenv('BANXICO_API_KEY')
BANXICO_SERIES = getenv('BANXICO_SERIES')
TIMEZONE = getenv('TIMEZONE', 'America/Mexico_City')
