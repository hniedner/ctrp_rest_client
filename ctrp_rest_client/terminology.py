import sqlite3


# get connection to sqlite3 terminology database
def get_connection():
    connection = sqlite3.connect('db/terminology.db')
    connection.row_factory = sqlite3.Row
    return connection


# execute submitted sql that must retrieve a resultset
# with two fields named 'code' and 'name'
# function returns [{code: 'code1', name: 'name1'}, {code: 'code2', name: 'name2'}, ...]
def get_code_name_list_result(sql):
    connection = get_connection()
    results = []
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            results.append({'code': row['code'], 'name': row['name']})
        cursor.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    return results


def get_single_string_result(sql):
    connection = get_connection()
    result = None
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    return result


def search_cancertypes_by_substring(query):
    sql = "select code, name from neoplasm_core where name like '%" \
          + query + "%' or synonyms like '%" + query + "%'"
    results = get_code_name_list_result(sql)
    return results


def search_biomarkers_by_substring(query):
    sql = "select code, name from biomarkers where name like '%" \
          + query + "%'"
    results = get_code_name_list_result(sql)
    return results


def expand_code_subtree(code):
    sql = "select code, name from ncit where parent_codes like '%" \
          + code + "%'"
    results = get_code_name_list_result(sql)
    return results


def get_name_for_code(domain, code):
    if domain == 'biomarkers':
        table = 'biomarkers'
    elif domain == 'diseases':
        table = 'neoplasm_core'
    else:
        table = 'ncit'

    sql = "select name from " + table + " where code = '" + code + "'"
    name = get_single_string_result(sql)

    if name:
        return name

    sql = "select name from ncit where code = '" + code + "'"
    name = get_single_string_result(sql)

    return name
