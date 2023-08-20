# Google BigQuery service account key json file
import os


class TestConfig(object):
    settings = ['BQ_SA_KEY_JSON_FILE']
    BQ_SA_KEY_JSON_FILE = os.environ.get('TEST_BQ_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_bq_tests.json'

    def to_dict(self):
        r = {}
        for k in self.settings:
            r[k] = self.__getattribute__(k)
        return r



