# API TO CONNECT TO BUDA'S PUBLIC API: Spread challenge.

## To Run:

Clone this repo.

Copy .dev_env content into a .env file and add a ficticial API **secret_key**

In root, build docker image running in bash:

```bash
docker-compose up --build -d
```

Create user by running in Docker container shell (not necessary to hit the API):

```docker
python manage.py createsuperuser
```

Access the admin view browsing to: http://localhost:5000/admin (to check spreads threshold alert)

## Hit the API:

- Single market spread:
  http://localhost:5000/api/tobuda/?secret=[secret_key]&market_id=[desired_market_id]
- Every available market spread:
  http://localhost:5000/api/tobuda/all/?secret=[secret_key]
