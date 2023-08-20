import base64
import datetime


class BigQueryContent:

    def __init__(self, *args, **kwargs):
        self.data = None
        self.last_run = None
        self.title = None
        self.sql_query = None

        if 'sql_query' in kwargs:
            self.sql_query = kwargs.get('sql_query')

        if 'title' in kwargs:
            self.title = kwargs.get('title')


def singleton(cls):
    obj = cls()
    # Always return the same object
    cls.__new__ = staticmethod(lambda cls: obj)
    # Disable __init__
    try:
        del cls.__init__
    except AttributeError:
        pass
    return cls


@singleton
class AppBQContentManager:
    # Big Query Connection manager
    bq = None

    def __init__(self, *args, **kwargs):
        self.app = None
        self.app_id = None
        self.titles = None
        self.sql_queries = None
        self.load_titles()
        self.load_sql_queries()

        # content: In memory BiqQueryContent objects dictionary
        self.contents = {}

    def init_app(self, app, bq):
        self.app = app
        self.app_id = app.config.get('VIEW_APP_NAME')
        self.__class__.bq = bq

    def bq_run(self, sql_query):
        # Only run in BQ  if not run already today or empty data
        bq = self.__class__.bq
        data = None
        if sql_query is not None and bq.initialized():
            try:
                query_job = self.bq.client.query(query=sql_query)
                # Wait for job with default timeout and retry policy
                while query_job.done() is False:
                    pass
                # Format job results
                # Result is a group of rows
                output = []
                for row in query_job.result():
                    # Row values can be accessed by field name or index.
                    output.append(row)
                data = [dict(row) for row in output]
            except Exception as e:
                print("Exception {}:{} Method: {}".format(e.__class__, e, self.bq_run.__name__))
                data = None
        return data

    def load_content(self, key, *args, **kwargs):
        content_manager = self
        content_key = key

        # Title and query provided by Content Manager
        title = content_manager.titles.get(key)
        sql_query = content_manager.sql_queries.get(key)

        if 'country' in kwargs:
            country = kwargs.get('country')
            if country is not None:
                sql_query = sql_query.replace('<country>', country)
                # Key includes method name and country
                content_key = content_key + '@' + country.lower()

        # print("Content_key: {}".format(content_key))
        # See if a local BigQueryContent exists in local content_manager
        local_content = content_manager.contents.get(content_key)
        if local_content is None:
            # Create object in local runner memory
            local_content = BigQueryContent(sql_query=sql_query, title=title)
            # Effectively run BiqQuery call with SQL query
            local_content.data = self.bq_run(sql_query=sql_query)
            local_content.last_run = datetime.date.today()
            # Register local_content  in content_manager
            content_manager.contents.update({content_key: local_content})
        else:
            # Already in local runner memory
            # Here check freshness and see whether it needs re-running
            # print("Content already in local runner memory:{}  ".format(local_content.last_run))
            if isinstance(local_content, BigQueryContent):
                if local_content.last_run != datetime.date.today() or local_content.data is None:
                    # bq_run could return None in case of BQ error
                    new_data = self.bq_run(sql_query=sql_query)
                    if new_data is not None:
                        local_content.data = new_data
                        local_content.last_run = datetime.date.today()
        payload = local_content.data
        return payload

    def load_titles(self):
        titles = {}
        titles.update({"get_countries_ranking": "Top 5 countries by total cases"})
        titles.update({"get_countries": "List of countries"})
        titles.update({"get_country_latest_date": "Latest date available"})
        titles.update({"get_country_summary": "Country summary"})
        self.titles = titles

    def load_sql_queries(self):
        sql_queries = {}
        sql_queries.update({"get_countries_ranking": """WITH available  AS
            (
            SELECT MAX(date) as latest_date_published
            FROM `bigquery-public-data.covid19_jhu_csse_eu.summary` 
            )
        SELECT country_region,  CAST(MAX(date) AS STRING)  as latest, SUM(confirmed) as cases, SUM(deaths)  as dead, 100*SAFE_DIVIDE(SUM(deaths),SUM(confirmed)) as drate
        FROM `bigquery-public-data.covid19_jhu_csse_eu.summary`,  available
        WHERE date=latest_date_published
        GROUP BY country_region
        ORDER BY cases DESC, dead DESC
        LIMIT 5"""})
        sql_queries.update({"get_countries": """SELECT DISTINCT country_region 
                        FROM `bigquery-public-data.covid19_jhu_csse_eu.summary`
                        WHERE DATE_DIFF(CURRENT_DATE(), date, YEAR)<1
                         ORDER BY country_region ASC"""})
        sql_queries.update({"get_country_latest_date": """SELECT CAST (MAX(date) AS STRING)  as latest_date
                        FROM `bigquery-public-data.covid19_jhu_csse_eu.summary` 
                        WHERE country_region='<country>'"""})
        sql_queries.update({"get_country_summary": """WITH available  AS
            (
            SELECT MAX(date) as latest_date_published
            FROM `bigquery-public-data.covid19_jhu_csse_eu.summary` 
            WHERE country_region='<country>'
            )
        SELECT country_region, CAST(MAX(date) AS STRING) as latest, SUM(confirmed) as cases, SUM(deaths)  as dead,  100*SAFE_DIVIDE(SUM(deaths),SUM(confirmed)) as drate
        FROM `bigquery-public-data.covid19_jhu_csse_eu.summary`,  available
        WHERE country_region='<country>' AND date=latest_date_published
        GROUP BY country_region"""})
        self.sql_queries = sql_queries