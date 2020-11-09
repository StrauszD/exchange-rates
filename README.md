# Exchange Rates

This API returns exchange rates according to different sources.

1. [Built With](#built-with)
2. [Deployment](#deployment)
3. [Usage](#usage)
4. [Author](#author)

## Built With

- [Auth0 - Secure access for everyone](https://auth0.com/)
- [BeautifulSoup - Library that makes it easy to scrape information from web pages.](https://pypi.org/project/beautifulsoup4/)
- [Docker - Container Framework](https://www.docker.com/)
- [Flask - Lightweight WSGI web application framework.](http://flask.palletsprojects.com/en/1.1.x/)
- [Redis - Open source in-memory data structure store](https://redis.io/)


## Deployment
To run the project locally you have to follow the following instructions 

Set the following environment variables:

```
FIXER_API_KEY=

BANXICO_API_KEY=

BANXICO_SERIES=SF43718

AUTH0_CLIENT_ID=

AUTH0_CLIENT_SECRET=

REDIS_USRL=
```

Then initialize API requirements:

```bash
docker-compose up
```

Then run the application:
```bash
python3 app.py
```

## Usage
This micro-service has two endpoints:

* **Endpoint `{{host}}/api/v1/exchange-rate/usd-rates, [GET]`**
   
   API calls limited to 15 in 3 minutes per user
   
   This endpoint returns the USD to MXN values for the current day.

   Banxico API does not return information on weekends so it will return the values in null when consulted on a weekend

   Headers:
   ````json
   {
      "Authorization": "Bearer <token>",
      "User": "<user>" 
   }
   ````

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
  
    cURL:
    ```shell script
    curl --location --request GET '{{host}}/api/v1/exchange-rate/usd-rates' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <token>' \
    --header 'User: 1'
    ```

* Endpoint `{{host}}/api/v1/exchange-rate/token, [GET]`
    
    This endpoint returns an Auth0 token to access the previous endpoint
    
    Response Body:
    ````json
    {
        "access_token": "token",
        "expires_in": 86400,
        "token_type": "Bearer"
    }
    ````
  
  cURL:
  ````shell script
    curl --location --request GET '{{host}}/api/v1/exchange-rate/token'
    ````

## Author
- Daniel Strausz - danst.1199@gmail.com
