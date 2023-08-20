# Google BigQuery service account key json file
import os


class Config(object):
    settings = ['BQ_SA_KEY_JSON_FILE',  'VIEW_APP_NAME', 'FLASK_APP_DISPLAY_NAME']
    BQ_SA_KEY_JSON_FILE = os.environ.get('BQ_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_bq.json'
    VIEW_APP_NAME = os.environ.get('VIEW_APP_NAME') or 'gcpBQDemo'
    FLASK_APP_DISPLAY_NAME = os.environ.get('FLASK_APP_DISPLAY_NAME') or VIEW_APP_NAME
    # Recommended generating key before running server
    # export  FLASK_SECRET_KEY =$(openssl rand -base64 128 | tee /secrets_storage_path/flask_secret_key.log)
    # It generates a strong key and record its value to variable and file both

    # The Config object key for the Flask app must be called SECRET_KEY, regardless of the OS environment variable name

    # Start of Flask configuration..................................................
    # Flask Config keys and values
    # Cannot use programmatic random SECRET_KEYS with multiple gunicorn workers
    # since every worker will generate a different random key
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT') or True
    SESSION_TYPE = os.environ.get('SESSION_TYPE') or "filesystem"

    # End of Flask configuration....................................................

    def to_dict(self):
        r = {}
        for k in self.settings:
            r[k] = self.__getattribute__(k)
        return r

