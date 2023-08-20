from app import app_bq_cm


def country_list() -> object:
    content_data, title = get_countries()
    if content_data:
        return content_data


def get_countries() -> tuple:
    key = 'get_countries'
    content_data = app_bq_cm.load_content(key=key)
    title = app_bq_cm.titles.get(key)
    return content_data, title


def get_preview_items() -> tuple:
    # Choose a key from Content Manager to choose as preview
    # Must be a key without parameters (country, start_date, etc.)
    key = 'get_countries_ranking'
    content_data = app_bq_cm.load_content(key=key)
    title = app_bq_cm.titles.get(key)
    return content_data, title


def get_country_summary(country: str) -> tuple:
    # Total cases confirmed for latest date published for  country
    # List of territories for country
    key = 'get_country_summary'
    content_data = app_bq_cm.load_content(key=key, country=country)
    title = app_bq_cm.titles.get(key)
    return content_data, title
