import flask
from flask import render_template, redirect, url_for, request, current_app, jsonify
from app.main import bp
from app.main.forms import ChooseCountryForm, format_countries_list
from bq_interface import get_country_summary, get_preview_items, country_list
from base64 import urlsafe_b64decode, urlsafe_b64encode


@bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    payload = {"status": "OK"}
    return jsonify(payload)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    # Recover browser session cookie
    # latest_content stores the latest country displayed
    latest_content = None
    latest_content_rx = request.cookies.get('latest_content')
    if latest_content_rx:
        latest_content = urlsafe_b64decode(latest_content_rx).decode()
    # latest_content_rx is a string representation of base64
    # urlsafe_b64decode accepts a string as parameter
    # decoding to convert bytes representing characters with system default decoder (example: UTF-8)
    # str ->bytes ->str

    query_form = ChooseCountryForm()
    # Form is populated with BigQueryContent data provided by the BigQueryContentManager
    query_form.populate_form_with_choices(choices=format_countries_list(country_list()))

    # Preview is not static, so it's loaded on every request
    # Basic cache in place by BigQueryContentManager
    display_content_items, display_content_title = get_preview_items()
    # reset_keyword cannot be a country
    reset_keyword="TOP_RANKING"

    # GET method
    if request.method == 'GET':
        if latest_content and latest_content != reset_keyword:
            # Pre-populate form with the last country option
            query_form.country.data = latest_content
            display_content_items, display_content_title = get_country_summary(country=latest_content)

    # POST method
    if query_form.validate_on_submit():
        country = query_form.country.data
        reset_display = query_form.ranking.data
        # Store latest content info to Cookie
        # Could use sessions if using user authentication with Flask login
        if reset_display:
            latest_content = reset_keyword
        else:
            latest_content = country
        response = redirect(url_for('main.index'))
        response.set_cookie(key='latest_content', value=urlsafe_b64encode(latest_content.encode()))
        return response

    view_app_name = current_app.config.get('VIEW_APP_NAME')
    return render_template('main/index.html', title='COVID stats by country', display_app_name=view_app_name,
                           form=query_form, content_items=display_content_items, content_title=display_content_title)


@bp.route('/favicon.ico')
def favicon():
    # Alternatively redirect to a static content route
    return flask.send_file('static/pictures/favicon.ico')


@bp.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
