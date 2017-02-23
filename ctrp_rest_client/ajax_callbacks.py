import sqlite3

from flask import jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField

from ctrp_rest_client import app


class TestForm(FlaskForm):
    disease = StringField(u'Disease')
    submit = SubmitField(u'Search')
    disease_codes = HiddenField()


@app.route('/search_diseases')
def search_disease():
    connection = sqlite3.connect('db/terminology.db')
    connection.row_factory = sqlite3.Row

    query = request.args.get('q')
    result = []

    try:
        cursor = connection.cursor()
        sql = "select code data, preferred_term value from neoplasm_core where preferred_term like '%" \
              + query + "%' or synonyms like '%" + query + "%'"

        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({'value': row['value'], 'data': row['data']})

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    return jsonify(result)


@app.route('/search_biomarkers')
def search_biomarkers():
    connection = sqlite3.connect('db/terminology.db')
    connection.row_factory = sqlite3.Row

    query = request.args.get('q')
    result = []

    try:
        cursor = connection.cursor()
        sql = "select code data, name value from biomarkers where name like '%" \
              + query + "%'"

        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({'value': row['value'], 'data': row['data']})

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    return jsonify(result)
