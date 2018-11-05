# Vison API app engine standar Python 3.7

## Installation

Require:
- Python 2.7 for run app engine
- Python 3.7 for code
- pip


```bash
python3.7 -m pip install -r requirements.txt -t lib --upgrade;
```
## Run

```bash
# Enviroment var is not working currently
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credential.json";

dev_appserver.py ./;
```

## Deploy

```bash
 gcloud app deploy ./;
```
