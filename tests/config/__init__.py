# Google BigQuery service account key json file
import os


class TestConfig(object):
    settings = ['BQ_SA_KEY_JSON_FILE',  'VIEW_APP_NAME', 'FLASK_APP_DISPLAY_NAME']
    BQ_SA_KEY_JSON_FILE = os.environ.get('TEST_BQ_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_bq_tests.json'
    VIEW_APP_NAME = os.environ.get('VIEW_APP_NAME') or 'gcpBQDemo'
    FLASK_APP_DISPLAY_NAME = os.environ.get('FLASK_APP_DISPLAY_NAME') or VIEW_APP_NAME

    def to_dict(self):
        r = {}
        for k in self.settings:
            r[k] = self.__getattribute__(k)
        return r



