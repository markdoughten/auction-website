Auction website

A user can buy and sell planes.

## Frontend

[frontend](https://angular.dev/installation) - 

```
ng install
``` 

The frontend requires nodejs, npm, angular.

run ``ng s`` when developing.

## Backend

[backend](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/):

```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
deactivate
```

run `serve.sh` when developing

Run `curl "http://localhost:5000/seed/all" -X "POST"` to seed dummy data in the DB.

Here is the database schema:
![1](/docs/images/schema.png)
