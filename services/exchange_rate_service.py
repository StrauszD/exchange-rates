from services.diario_oficial_service import DiarioOficialService
from services.fixer_service import FixerService
from services.banxico_service import BanxicoService

fixer = FixerService()
banxico = BanxicoService()
diario_oficial = DiarioOficialService()


class ExchangeRateService:

    @staticmethod
    def get_usd_rates():
        fixer_rate = fixer.get_usd_rate().__dict__
        banxico_rate = banxico.get_usd_rate().__dict__
        diario_oficial_rate = diario_oficial.get_usd_rate().__dict__

        return {
            'rates': {
                'fixer': fixer_rate,
                'banxico': banxico_rate,
                'diario_oficial': diario_oficial_rate
            }
        }
