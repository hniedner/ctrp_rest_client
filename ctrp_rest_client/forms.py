from flask_wtf import FlaskForm
from wtforms import validators, StringField, SubmitField, BooleanField, SelectField, IntegerField


class TrialSearchForm(FlaskForm):
    gender_choices = [('Any', 'Any'), ('Both', 'Both'), ('Male', 'Male'), ('Female', 'Female')]
    healthy_volunteer_choices = [('NA', 'NA'), ('Yes', 'Yes'), ('No', 'No')]

    fulltext = StringField(u'Keywords')

    disease_codes = StringField(u'NCI Thesaurus Disease Codes (comma separated list)')

    biomarker_codes = StringField(u'NCI Thesaurus Biomarker Codes (comma separated list)')
    biomarker_assay_purpose_inclusion = BooleanField(u'Biomarker Inclusion Criterion')
    biomarker_assay_purpose_exclusion = BooleanField(u'Biomarker Exclusion Criterion')

    gender = SelectField(u'Gender', choices=gender_choices, default='Any')

    phasena = BooleanField(u'Phase NA')
    phase0 = BooleanField(u'Phase 0')
    phase1 = BooleanField(u'Phase I')
    phase2 = BooleanField(u'Phase 2')
    phase3 = BooleanField(u'Phase 3')
    phase4 = BooleanField(u'Phase 4')
    submit = SubmitField(u'Search')

    # apparently IntegerField is required by default
    min_age_number = IntegerField(u'Minimum Age in years', validators=[validators.optional()])
    max_age_number = IntegerField(u'Maximum Age in years', validators=[validators.optional()])

    accepts_healthy_volunteers_indicator = SelectField('Accepts Healthy Volunteers',
                                                       choices=healthy_volunteer_choices,
                                                       default='NA')
