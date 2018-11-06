# Vison API AppEngine Standar Python 3.7

## Installation

### Firebase and GCP
- Create GCP Project ([Console](https://console.cloud.google.com))
- Create Firebase Project ([Console](https://console.firebase.google.com/u/0/?hl=es-419&pli=1) | [Doc](https://firebase.google.com/docs/web/setup?hl=es-419))
    - Start with Firebase ([Doc](https://firebase.google.com/docs/storage/web/start?hl=es-419))
    - Add App (+), copy and paste code in `<head>` html tag


### Require:
- **Python 2.7** for run App Engine local
- **Python 3.7** for run code
- **pip** to install python dependences
- **Browser file API** ((doc)[https://www.html5rocks.com/es/tutorials/file/dndfiles/])


```bash
python3.7 -m pip install -r requirements.txt -t lib --upgrade;
```

### Create constants files
- **static/js/constants.js**
    ```javascript
    # From firebase
    const FIREBASE_CONFIG = {
        apiKey: "AIz...",
        authDomain: "<PROJEC_ID>.firebaseapp.com",
        databaseURL: "https://<PROJEC_ID>.firebaseio.com",
        projectId: "<PROJEC_ID>",
        storageBucket: "<PROJEC_ID>.appspot.com",
        messagingSenderId: "000..."
    };
    const BUCKET_DIR = 'sub_directory';
    
    ```
- **app_vision/constants.py**
    ```python
    import sys

    ROOT_PATH = sys.path[0]
    BUCKET_DIR = 'sub_directory'
    BUCKET = 'gs://<PROJEC_ID>.appspot.com/' + BUCKET_DIR
    CREDENTIAL_JSON = 'credential.json'
    ```
- **credential.json**
    ```json
    {
    "type": "service_account",
    "project_id": "...",
    "private_key_id": "...",
    "private_key": "...",
    "client_email": "...",
    "client_id": "...",
    "auth_uri": "...",
    "token_uri": "...",
    "auth_provider_x509_cert_url": "...",
    "client_x509_cert_url": "..."
    }
    ```

## Run

```bash
# Enviroment var is not working currently
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credential.json";

dev_appserver.py ./;

# test
curl http://localhost:8080/get-image/tomaco_man.jpg;
```

## Deploy

```bash
 gcloud app deploy ./;
```
