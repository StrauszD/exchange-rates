import logging
import traceback

from services.auth_service import AuthService
from settings import BASE_ROUTE
from flask import Blueprint, jsonify

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

auth_blueprint = Blueprint('auth_blueprint', 'auth_blueprint')
auth_service = AuthService()


@auth_blueprint.route(f'/{BASE_ROUTE}/token', methods=['GET'])
def get_token():
    try:
        res = auth_service.get_token()
        return jsonify(res), 200
    except Exception as error:
        logging.error(f'Error while getting exchange rate {str(error)}')
        logging.error(traceback.format_exc())

        return jsonify({'message': str(error)}), 500
