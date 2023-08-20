# gfs-bq-manager
#### A simple Google Cloud BigQuery manager

## Connecting your application to Google Cloud BigQuery
A basic connection manager to leverage [BigQuery API Client Libraries](https://cloud.google.com/bigquery/docs/reference/libraries)
to use [BigQuery](https://cloud.google.com/bigquery/)  content for python applications.


## GBQManager class
**GBQManager**
1. Creates a  BigQuery API client from a service account key file  
*Note: required IAM roles for service account: BigQuery User*
2. Isolates BigQuery connections management

**Class use example to manage BigQuery connections for an app**  

*Link GBQManager to app*
```python
    # App specific
    # Link GBQManager to app
    bq = GBQManager()
    bq.init_app(app)
```

#### Seamlessly running query jobs in BigQuery from applications
*Use GBQManager to run BigQuery SQL query jobs*    
```python    
    sql_query = """SELECT DISTINCT country_region  
                FROM `bigquery-public-data.covid19_jhu_csse_eu.summary`  
                ORDER BY country_region ASC""" 
    query_job = bq.client.query(query=sql_query)
```

#### Configuring your application
**Application**
* Any object that has a 'config' property which is a dictionary
* Custom keys and values can be added to 'config'
* Example: could be a Flask app, a FastAPI app, etc.* 


**App configuration keys used by GBQManager class**
```console
   # Google Cloud Logging service account key json file
   # Determines service account and hence BigQuery project permissions
    BQ_SA_KEY_JSON_FILE = os.environ.get('LG_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_bq.json'
    
    # If defined and empty, application uses Application Default Credentials
    BQ_SA_KEY_JSON_FILE = ''
 ```

**Reference**  
* [Authenticating as a service account](https://cloud.google.com/docs/authentication/production#auth-cloud-explicit-python)
* [Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials)
* [Service Account(SA) key](https://cloud.google.com/iam/docs/keys-create-delete)

