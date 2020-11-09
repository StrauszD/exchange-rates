from os import getenv

BASE_ROUTE = getenv('BASE_ROUTE', 'api/v1/exchange-rate')
FIXER_API_KEY = getenv('FIXER_API_KEY')
BANXICO_API_KEY = getenv('BANXICO_API_KEY')
BANXICO_SERIES = getenv('BANXICO_SERIES')
AUTH0_CLIENT_ID = getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = getenv('AUTH0_CLIENT_SECRET')
REDIS_URL = getenv('REDIS_URL', 'redis://localhost:6379')
