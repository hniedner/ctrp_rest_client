import logging
import sqlite3
import ruamel.yaml

# create logger
logger = logging.getLogger('terminology')
# cashes sql and root concepts
data = {}


def load_terminology_data():
    global data
    f = open('terminology.yml', 'r')
    data = ruamel.yaml.safe_load(f.read())
    f.close()
    return data


def get_dom_sql(dom):
    global data
    if len(data) == 0:
        load_terminology_data()
    return data['dom_sql'][dom]


def get_sql(query):
    global data
    if len(data) == 0:
        load_terminology_data()
    return data['sql'][query]


def get_root_concept(dom):
    global data
    if len(data) == 0:
        load_terminology_data()
    if data['root_concept'][dom]:
        return data['root_concept'][dom]
    else:
        return data['root_concept_default']


# if code (concept id) is 'root' replace with NCIt root concept
def check_for_root(code, dom):
    if 'root' == code:
        return get_root_concept(dom)['code']
    return code


# get connection to sqlite3 terminology database
def get_connection():
    connection = sqlite3.connect('db/terminology.db')
    connection.row_factory = sqlite3.Row
    return connection


# execute submitted sql that must retrieve a resultset
# with two fields named 'code' and 'name'
# function returns [{code: 'code1', name: 'name1'}, {code: 'code2', name: 'name2'}, ...]
def get_code_name_list_result(sql, querytokens=None):
    connection = get_connection()
    results = []
    try:
        cursor = connection.cursor()
        if querytokens:
            cursor.execute(sql, querytokens)
        else:
            cursor.execute(sql)
        for row in cursor.fetchall():
            results.append({'code': row['code'], 'name': row['name']})
        cursor.close()
    except sqlite3.Error as e:
        logger.error("An error occurred:", e.args)
    return results


# get a single row or a single field as a string
def get_single_string_result(sql, querytokens=None):
    connection = get_connection()
    result = None
    try:
        cursor = connection.cursor()
        if querytokens:
            cursor.execute(sql, querytokens)
        else:
            cursor.execute(sql)
        if cursor.arraysize > 0:
            result = cursor.fetchone()[0]
        cursor.close()
    except sqlite3.Error as e:
        logger.error("An error occurred:", e.args[0])
    return result


def search_domain_by_substring(dom, query):
    return get_code_name_list_result(get_dom_sql(dom), ['%' + query + '%', '%' + query + '%'])


def search_diseases_associated_with_anatomic_site(code):
    return get_code_name_list_result(get_sql('search_diseases_associated_with_anatomic_site'),
                                     [check_for_root(code, 'anantomicsite')])


def search_diseases_associated_with_finding(code):
    return get_code_name_list_result(get_sql('search_diseases_associated_with_finding'),
                                     [check_for_root(code, 'finding')])


def search_diseases_associated_with_gene(code):
    return get_code_name_list_result(get_sql('search_diseases_associated_with_gene'),
                                     [check_for_root(code, 'gene')])


def search_diseases_is_stage(code):
    return get_code_name_list_result(get_sql('search_diseases_is_stage'),
                                     [check_for_root(code, 'disease')])


def search_diseases_is_grade(code):
    return get_code_name_list_result(get_sql('search_diseases_is_grade'),
                                     [check_for_root(code, 'disease')])


def get_subtree_codes(code, dom):
    connection = sqlite3.connect('db/terminology.db')
    connection.row_factory = lambda cursor, row: row[0]
    results = []
    try:
        cursor = connection.cursor()
        cursor.execute(get_sql('get_subtree_codes'), [check_for_root(code, dom)])
        results = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as e:
        logger.error("An error occurred:", e)
    return results


def get_child_codes(code, dom):
    # biomarkers are not marked up as such in ncit so we return all flat
    ccode = check_for_root(code, dom)
    # parent codes are in a pipe (|) delimited list
    # just matching on the first term we get spurious substring matches
    # such as C8461 matching C84615
    return get_code_name_list_result(get_sql('get_child_codes'), ['%' + ccode, '%' + ccode + '|%'])


def get_parent_codes(code, dom):
    ccode = check_for_root(code, dom)
    parent_codes = get_single_string_result(get_sql('get_parent_codes'), [ccode])
    results = []
    # parent codes are in a pipe (|) delimited list
    for parent_code in parent_codes.split('|'):
        results.extend(get_code_name_list_result(get_sql('get_parent_codes_sub'), [parent_code]))
    return results
