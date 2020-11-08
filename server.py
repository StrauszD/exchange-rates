from flask import Flask
import logging
from blueprints.exchange_rate_blueprint import exchange_rate_blueprint

app = Flask(__name__)
app.register_blueprint(exchange_rate_blueprint)

if __name__ == '__main__':
    logging.info('Starting Application')

    app.run(host='0.0.0.0', port=8080)
