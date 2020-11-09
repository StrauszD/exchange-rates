from flask import Flask, jsonify
import logging
from controllers.auth_controller import auth_blueprint
from controllers.exchange_rate_controller import exchange_rate_blueprint
from entities.auth_error import AuthError
from entities.rate_limit_error import RateLimitError

app = Flask(__name__)
app.register_blueprint(exchange_rate_blueprint)
app.register_blueprint(auth_blueprint)


@app.errorhandler(AuthError)
@app.errorhandler(RateLimitError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code

    return response


if __name__ == '__main__':
    logging.info('Starting Application')

    app.run(host='0.0.0.0', port=8080)
