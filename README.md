# Vison API AppEngine Standar Python 3.7

## Installation

### Firebase and GCP
- Create GCP Project ([Console](https://console.cloud.google.com))
- Create Firebase Project ([Console](https://console.firebase.google.com/u/0/?hl=es-419&pli=1) | [Doc](https://firebase.google.com/docs/web/setup?hl=es-419))
    - Start with Firebase ([Doc](https://firebase.google.com/docs/storage/web/start?hl=es-419))
    - Add App (+), copy and paste code in `<head>` html tag


### Require:
- **Python 2.7** for run App Engine local
- **Python 3.7** like python3
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
  
    PROJECT_ID = '<PROJECT_ID>'
    BUCKET_DIR = 'sub_directory'
    BUCKET = 'gs://<PROJECT_ID>.appspot.com/' + BUCKET_DIR
    CREDENTIAL_JSON = 'credential.json'
    CLIENT_SECRET_JSON = '....apps.googleusercontent.com.json'
    CLIENT_SECRET_FILE = sys.path[0] + '/' + CLIENT_SECRET_JSON
    GOOGLE_APPLICATION_CREDENTIALS = sys.path[0] + '/' + CREDENTIAL_JSON
    CLIENT_SECRET = 'qwe8G...' # from GCP Client secret
    SPREAD_SHEET = '19qw...' # Id for spread sheet
    SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/spreadsheets.readonly']
        
    ```
    
- **config.py**
    ```python
    import os
    from app_vision.constants import GOOGLE_APPLICATION_CREDENTIALS

    # For local debug
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    SECRET_KEY = 'super secret key'
  
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

dev_appserver.py ./ --host="0.0.0.0" --enable_host_checking="false" --log_level="debug";

# test
curl http://localhost:8080/get-image/tomaco_man.jpg;
```

## Edit Frontend
- install **nodejs 8+** and dependencies
    ```bash
    npm i -g stylus nib pug-cli less less-prefixer watch-less http-server bower;
    ```
- html render from pug
    ```bash
    pug -w -P -o ./app_vision/templates/ ./app_vision/templates/index.pug;
    ```
- css rednder from stylus
    ```bash
    stylus -u nib -w ./static/css/style.styl
    ```

## Deploy

```bash
 gcloud app deploy ./;
```
