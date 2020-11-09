import requests
from settings import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET


class AuthService:
    @staticmethod
    def get_token():
        uri = 'https://exchange-rates.us.auth0.com/oauth/token'
        data = {
            'client_id': AUTH0_CLIENT_ID,
            'client_secret': AUTH0_CLIENT_SECRET,
            'audience': 'https://exchange-rates/api',
            'grant_type': 'client_credentials'
        }

        return requests.post(uri, data).json()
