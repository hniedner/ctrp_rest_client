from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, BooleanField, SelectField


class TrialSearchForm(FlaskForm):
    gender_choices = [('Any', 'Any'), ('Both', 'Both'), ('Male', 'Male'), ('Female', 'Female')]
    healthy_volunteer_choices = [('NA', 'NA'), ('Yes', 'Yes'), ('No', 'No')]

    disease_code = StringField(u'NCI Thesaurus Disease Code', validators=[validators.DataRequired()])
    accepts_healthy_volunteers_indicator = SelectField('Accepts Healthy Volunteers', choices=healthy_volunteer_choices,
                                                       default='NA')
    gender = SelectField(u'Gender', choices=gender_choices, default='Any')
    phasena = BooleanField(u'Phase NA')
    phase0 = BooleanField(u'Phase 0')
    phase1 = BooleanField(u'Phase I')
    phase2 = BooleanField(u'Phase 2')
    phase3 = BooleanField(u'Phase 3')
    phase4 = BooleanField(u'Phase 4')
    submit = SubmitField("Search")
