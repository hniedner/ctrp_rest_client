import sqlite3

from flask import jsonify, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField

from ctrp_rest_client import app


class TestForm(FlaskForm):
    disease = StringField(u'Disease')
    submit = SubmitField(u'Search')
    disease_codes = HiddenField()


def get_connection():
    connection = sqlite3.connect('db/terminology.db')
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/search_diseases')
def search_disease():
    connection = get_connection()

    query = request.args.get('q')
    result = []

    try:
        cursor = connection.cursor()
        sql = "select code data, name value from neoplasm_core where name like '%" \
              + query + "%' or synonyms like '%" + query + "%'"

        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({'value': row['value'], 'data': row['data']})

        cursor.close()

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    return jsonify(result)


@app.route('/search_biomarkers')
def search_biomarkers():
    connection = get_connection()

    query = request.args.get('q')
    result = []

    try:
        cursor = connection.cursor()
        sql = "select code data, name value from biomarkers where name like '%" \
              + query + "%'"

        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({'value': row['value'], 'data': row['data']})

        cursor.close()

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    return jsonify(result)


@app.route('/expand_ncit_code')
def expand_ncit_code():
    connection = get_connection()

    code = request.args.get('code')
    result = []

    try:
        cursor = connection.cursor()
        sql = "select code data, name value from ncit where parent_codes like '%" \
              + code + "%'"

        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({'value': row['value'], 'data': row['data']})

        cursor.close()

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    return jsonify(result)


@app.route('/get_name_for_ncit_code')
def get_name_for_ncit_code():
    connection = get_connection()

    domain = request.args.get('dom')
    code = request.args.get('code')

    if domain == 'biomarkers':
        table = 'biomarkers'
    elif domain == 'diseases':
        table = 'neoplasm_core'
    else:
        table = 'ncit'

    try:
        cursor = connection.cursor()
        sql = "select name from " + table + " where code = '" + code + "'"
        cursor.execute(sql)

        result = cursor.fetchone()['name']

        if not result:
            cursor.close()
            cursor = connection.cursor()
            sql = "select name from ncit where code = '" + code + "'"
            cursor.execute(sql)
            result = cursor.fetchone()['name']

        if result:
            name = result
        else:
            name = 'not found'

        cursor.close()

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])

    return jsonify(name)
