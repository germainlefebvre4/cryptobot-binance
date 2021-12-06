# Cryptobot Binance

## Getting started
Install required packages:
```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip install pipenv
```

Run the app:
```bash
pipenv update
pipenv run uvicorn app.main:app --port=8083 --reload
```


## Development

### Setup workspace
```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip install pipenv
pipenv update --dev
```

### Run locally
```bash
pipenv run uvicorn app.main:app --port=8083 --reload
```

### Run tests
```bash
pipenv run pytest -sv app/tests/
```
