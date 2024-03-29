# API TO CONNECT TO BUDA'S PUBLIC API: Spread challenge.

\*Assumptions: every requirement should be part of the API, meaning:

- There is an endpoint to GET single market spread and POST single market alert spread for future polling.
- There is an endpoint to GET every publicly available market spread in a single call.
- There is an endpoint to poll a single market and check if current spread is higher than saved alert spread for that market.

## To Run:

Clone this repo.

Copy _.dev_env_ content into a _.env_ file and add a fictitious API **secret_key** and the Buda API endpoint.

In root, build docker image running in bash:

```bash
docker-compose up --build -d
```

Create user by running in Docker container shell (not necessary to hit the API):

```docker
python manage.py createsuperuser
```

Access the admin view browsing to: http://localhost:5000/admin (to check spreads threshold alert). To log-in use dummy user: devdev, pass: 123456.

## Hit the API:

1. Ask for spreads:

- [Single market spread](http://localhost:5000/api/tobuda/?secret=[secret_key]&market_id=[desired_market_id])
- [Every available market spread](http://localhost:5000/api/tobuda/all/?secret=[secret_key])

2. Set alert spread:
   POST with postman or directly into the [Django DRF View](http://localhost:5000/api/tobuda):
   ```json
   {
   "secret": "[secret_key]",
   "market_id": "[desired_market_id]",
   "alert_spread": [spread_alert_value],
   "trading_currency": "[desired_market_id_currency]"
   }
   ```

Good use case would be to hit the GET single market spread endpoint and pass the resulting content as the POST content to the same endpoint to set spread alert.

3. [Run polling for a single market](http://localhost:5000/api/tobuda/poll/?secret=[secret_key]&market_id=[desired_market_id])

## Run unit tests:

\*Presumptions: no need to test DRF related libraries or include internet dependent tests.

Within the container run:

```docker
python manage.py test budapi.tests.test_api_tobuda
```
