# Using Google Cloud Big Query to add application content
#### Seamlessly running query jobs in BigQuery from applications   

## Add application content with BigQuery
A basic example of how to leverage [BigQuery API Client Libraries](https://cloud.google.com/bigquery/docs/reference/libraries) to produce content for the application.
It runs queries to a public dataset to generate content for an API or application.
As an example, a public dataset for worldwide CV19 infections statistics is queried to generate content served  upon request.

## Connecting your application to Google Cloud BigQuery

TODO: Summary on how to connect and use BigQuery in applications

## GBQManager class

**GBQManager**
1. Creates a  BigQuery API client from a service account key file
  *Note: required IAM roles for service account: BigQuery User*
2. Isolates BigQuery connections management

**Class use example to manage BigQuery connections for an app**  

*Link BigQueryManager to app*
```console
    # App specific
    # Link BigQueryManager to app
    bq = BigQueryManager()
    bq.init_app(self.app)
```


*Use BigQueryManager to run BigQuery query jobs*    
```console    
    sql_query = """SELECT DISTINCT country_region  
                FROM `bigquery-public-data.covid19_jhu_csse_eu.summary`  
                ORDER BY country_region ASC""" 
    query_job = bq.client.query(query=sql_query)
```


**App configuration keys used by BigQueryManager class**
```console
   # Application display name
    FLASK_APP_DISPLAY_NAME = os.environ.get('FLASK_APP_DISPLAY_NAME') or 'gcpBQDemo'
    
   # Google Cloud Logging service account key json file
   # Determines service account and hence BigQuery project permissions
    BQ_SA_KEY_JSON_FILE = os.environ.get('LG_SA_KEY_JSON_FILE') or '/etc/secrets/sa_key_bq.json'



 ```

## Running the application locally  

### Create Google Cloud resources
1. Create a [Google Cloud](https://console.cloud.google.com/home/dashboard)  platform account if you do not already have it.
2. [Create a Google Cloud project](https://developers.google.com/workspace/guides/create-project) or use an existing one.
3. Configure application identity
   * Create a [Service Account(SA) key](https://cloud.google.com/iam/docs/keys-create-delete)
   * Assign the IAM role BigQuery User to the SA during creation.
 


### Use Google Cloud Shell
To start coding right away, launch [Google Cloud Shell](https://console.cloud.google.com/home/).  

### Or use your own development environment
If you would rather use *your own local development machine* you will need to  [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstart) and Install Python

* Install python packages.

    ```console
    sudo apt update
    sudo apt install python3 python3-dev python3-venv
    ```
    
* Install pip 

    *Note*: Debian provides a package for pip

    ```console
    sudo apt install python-pip
    ```
    Alternatively pip can be installed with the following method
    ```console
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    ```
*Note: Console snippets for Debian/Ubuntu based distributions.*
### Clone git repo from Github
At this point either you are using Cloud Shell or you have a local development environment with python and Cloud SDK.
  ```console
  git clone https://github.com/amesones-dev/gfs-log-manager.git
   ```

### Create a pyhon virtual environment

User your cloned git repository folder for your source code and Python [venv](https://docs.python.org/3/library/venv.html)
virtual environment to isolate python dependencies. 

```console
cd gfs-log-manager
python -m venv [venv-name]
source [venv-name]/bin/activate
```
Usual values for [venv-name] are `venv`, `dvenv`, `venv39` for a python 3.9 version virtual environment, etc.

### Install python requirements
```console
# From gfs-log-manager/src folder
pip install -r requirements.txt
```


### App configuration
At this point you are ready to configure and run the application.
  * Edit the application configuration Config class to update the key LG_SA_KEY_JSON_FILE with the SA key file path 
  created in  [Create Google Cloud resources](#create-google-cloud-resources)

### Running the app
  * Set Flask environment variables
   ```console
   export  FLASK_SECRET_KEY=$(openssl rand -base64 128)
   export  FLASK_APP=app:create_app
   ```

  * Run with flask
   ```console
   flask run   
   ```

  * Or run with gunicorn
   ```console
   gunicorn start:app   
   ```






