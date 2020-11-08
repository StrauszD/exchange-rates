# Exchange Rates

This API returns exchange rates according to different sources.

1. [Built With](#built-with)
2. [Deployment](#deployment)
3. [Usage](#usage)
4. [Author](#author)

## Built With

- [BeautifulSoup - Library that makes it easy to scrape information from web pages.](https://pypi.org/project/beautifulsoup4/)
- [Flask - Flask is a lightweight WSGI web application framework.](http://flask.palletsprojects.com/en/1.1.x/)
- [Docker - Container Framework](https://www.docker.com/)


## Deployment
To deploy you have to set the following environment variables

FIXER_API_KEY=

BANXICO_API_KEY=

BANXICO_SERIES=SF43718

TIMEZONE=America/Mexico_City

First build the image as this:

```bash
docker build --force-rm -t exchange-rates .
```

Then run the image:

For Linux:
```bash
docker run -d -p 8080:8080 --env-file=.env --restart=always --name=exchange-rates exchange-rates
```

## Usage
This micro-service has one endpoint

Endpoint `{{host}}/api/v1/exchange-rate/usd-rates, [GET]`

This endpoint returns the USD to MXN values for the current day.

Banxico API does not return information on weekends so it will return the values in null when consulted on a weekend

Response body:
```json
{
    "rates": {
        "banxico": {
            "last_updated": "2020-11-07T00:00:00",
            "value": 20.76
        },
        "diario_oficial": {
            "last_updated": "2020-11-07T00:00:00",
            "value": 20.76
        },
        "fixer": {
            "last_updated": "2020-11-07T21:03:05",
            "value": 20.58
        }
    }
}
```

## Author
- Daniel Strausz - danst.1199@gmail.com
