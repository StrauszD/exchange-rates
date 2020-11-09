from app import app
import unittest
import json
from mockito import when

from entities.rate_entity import Rate
from decorators.rate_limit_decorator import redis
from services.exchange_rate_service import fixer, diario_oficial, banxico


class TestExchangeRate(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()
        redis.flush()

    def test_ok(self):
        # given
        get_token = json.loads(self.app.get('/api/v1/exchange-rate/token').data)
        access_token = get_token['access_token']
        auth_token = f'Bearer {access_token}'
        res = Rate(
            last_updated='2020-10-18T00:00:00',
            value=21.38
        )

        # when
        when(banxico).get_usd_rate(...).thenReturn(res)
        when(fixer).get_usd_rate(...).thenReturn(res)
        when(diario_oficial).get_usd_rate(...).thenReturn(res)

        response = self.app.get(
            '/api/v1/exchange-rate/usd-rates',
            headers={'user': '1', 'Authorization': auth_token}
        )

        # then
        assert 200 == response.status_code

    def test_unauthorized(self):
        # when
        response = self.app.get('/api/v1/exchange-rate/usd-rates', headers={'user': 'test', 'token': 'asd'})

        # then
        assert 401 == response.status_code

    def test_bad_headers(self):
        # when
        response = self.app.get('/api/v1/exchange-rate/usd-rates', headers={})

        # then
        assert 401 == response.status_code

    def test_rate_limit_exceeded(self):
        # given
        get_token = json.loads(self.app.get('/api/v1/exchange-rate/token').data)
        access_token = get_token['access_token']
        auth_token = f'Bearer {access_token}'
        res = Rate(
            last_updated='2020-10-18T00:00:00',
            value=21.38
        )

        # when
        when(banxico).get_usd_rate(...).thenReturn(res)
        when(fixer).get_usd_rate(...).thenReturn(res)
        when(diario_oficial).get_usd_rate(...).thenReturn(res)

        response = {}
        for i in range(17):
            response = self.app.get(
                '/api/v1/exchange-rate/usd-rates',
                headers={'user': '1', 'Authorization': auth_token}
            )

        # then
        assert 403 == response.status_code


if __name__ == '__main__':
    unittest.main()
