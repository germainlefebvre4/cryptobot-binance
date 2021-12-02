# Cryptobot Controller

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
pipenv run uvicorn app.main:app --port=8081 --reload
```

**Troubleshooting**

Some distributions might miss some packages. These are some hints if needed:
```bash
# cryptography/cffi
sudo apt install build-essential libssl-dev libffi-dev
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
This section use docker database called `cryptobot`.
```bash
pipenv run uvicorn app.main:app --port=8081 --reload
```

### Run tests
This section use docker database called `cryptobot_test`.
```bash
pipenv run pytest -sv app/tests/
```
