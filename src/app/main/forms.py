from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo


def format_countries_list(countries):
    # countries format:  [{'country_region':'Spain'},{'country_region':'France'}]
    form_choices = []
    for item in countries:
        form_choices.append(item.get('country_region'))
    return form_choices


class ChooseCountryForm(FlaskForm):
    country = SelectField(choices={}, validators=[DataRequired()])
    ranking = BooleanField(label="Reset view to Top Ranking")
    submit = SubmitField('Go')

    def populate_form_with_choices(self, choices):
        self.country.choices = choices
        self.ranking.choices = [('Top Ranking', 'Enable to reset display view to countries ranking by cases')]




