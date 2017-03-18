import sqlite3
import logging

# create logger
logger = logging.getLogger('terminology')


# if code (concept id) is 'root' replace with NCIt root concept
def check_for_root(code):
    if 'root' == code:
        return 'C7057'
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


def search_anatomicsite_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where semantic_type = "Anatomical Structure"' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_finding_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where semantic_type = "Finding"' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_cancertype_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where semantic_type = "Neoplastic Process" ' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_therapeutic_procedure_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where semantic_type = "Therapeutic or Preventive Procedure" ' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_diagnostic_procedure_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where semantic_type = "Diagnostic Procedure" ' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_laboratory_procedure_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where semantic_type = "Laboratory Procedure" ' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_drug_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where (semantic_type = "Pharmacologic Substance"' \
          'or semantic_type = "Pharmacologic Substance|Plant"' \
          'or semantic_type = "Pharmacologic Substance|Research Device"' \
          'or semantic_type = "Pharmacologic Substance|Steroid"' \
          'or semantic_type = "Pharmacologic Substance|Substance"' \
          'or semantic_type = "Pharmacologic Substance|Virus"' \
          'or semantic_type = "Pharmacologic Substance|Vitamin"' \
          'or semantic_type = "Organic Chemical|Pharmacologic Substance|Vitamin"' \
          'or semantic_type = "Organic Chemical|Pharmacologic Substance"' \
          'or semantic_type = "Nucleic Acid, Nucleoside, or Nucleotide|Pharmacologic Substance"' \
          'or semantic_type = "Inorganic Chemical|Pharmacologic Substance"' \
          'or semantic_type = "Immunologic Factor|Pharmacologic Substance"' \
          'or semantic_type = "Element, Ion, or Isotope|Pharmacologic Substance"' \
          'or semantic_type = "Clinical Drug"' \
          'or semantic_type = "Cell|Pharmacologic Substance"' \
          'or semantic_type = "Antibiotic|Pharmacologic Substance"' \
          'or semantic_type = "Amino Acid, Peptide, or Protein|Pharmacologic Substance"' \
          'or semantic_type = "Amino Acid, Peptide, or Protein|Immunologic Factor|Pharmacologic Substance")' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_biomarker_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where (semantic_type = "Acquired Abnormality" ' \
          'or semantic_type = "Amino Acid, Peptide, or Protein" ' \
          'or semantic_type = "Amino Acid, Peptide, or Protein|Biologically Active Substance" ' \
          'or semantic_type = "Amino Acid, Peptide, or Protein|Enzyme" ' \
          'or semantic_type = "Amino Acid, Peptide, or Protein|Enzyme|Receptor" ' \
          'or semantic_type = "Amino Acid, Peptide, or Protein|Hormone" ' \
          'or semantic_type = "Amino Acid, Peptide, or Protein|Immunologic Factor" ' \
          'or semantic_type = "Amino Acid, Peptide, or Protein|Receptor" ' \
          'or semantic_type = "Cell" ' \
          'or semantic_type = "Cell Component" ' \
          'or semantic_type = "Cell or Molecular Dysfunction" ' \
          'or semantic_type = "Clinical Attribute" ' \
          'or semantic_type = "Element, Ion, or Isotope" ' \
          'or semantic_type = "Finding" ' \
          'or semantic_type = "Functional Concept" ' \
          'or semantic_type = "Gene or Genome" ' \
          'or semantic_type = "Hazardous or Poisonous Substance|Inorganic Chemical" ' \
          'or semantic_type = "Hormone" ' \
          'or semantic_type = "Hormone|Organic Chemical" ' \
          'or semantic_type = "Immunologic Factor|Organic Chemical" ' \
          'or semantic_type = "Laboratory Procedure" ' \
          'or semantic_type = "Laboratory or Test Result" ' \
          'or semantic_type = "Nucleotide Sequence" ' \
          'or semantic_type = "Organic Chemical|Pharmacologic Substance" ' \
          'or semantic_type = "Pharmacologic Substance" ' \
          'or semantic_type = "Pharmacologic Substance|Vitamin" ' \
          'or semantic_type = "Virus") ' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_diseases_associated_with_anatomic_site(code):
    sql = 'SELECT DISTINCT rel.subject_code code, ncit.name name ' \
          'FROM ncit_relationships rel ' \
          'JOIN ncit ON rel.subject_code = ncit.code ' \
          'WHERE rel.object_code = ? ' \
          'AND (role = "Disease Has Associated Anatomic Site" ' \
          'OR role = "Disease Has Primary Anatomic Site" ' \
          'OR role = "Disease Has Metastatic Anatomic Site")'
    results = get_code_name_list_result(sql, [check_for_root(code)])
    return results


def search_diseases_associated_with_finding(code):
    sql = 'SELECT DISTINCT rel.subject_code code, ncit.name name ' \
          'FROM ncit_relationships rel ' \
          'JOIN ncit ON rel.subject_code = ncit.code ' \
          'WHERE rel.object_code = ? ' \
          'AND role = "Disease Has Finding"'
    return get_code_name_list_result(sql, [check_for_root(code)])


def search_diseases_associated_with_gene(code):
    sql = 'select rel.subject_code, ncit.name ' \
        'FROM ncit_relationships rel ' \
        'JOIN ncit ON ncit.code = rel.subject_code ' \
        'WHERE rel.object_code = ? ' \
        'AND (role = "Gene Associated With Disease" ' \
        'OR role = "Gene Involved In Pathogenesis Of Disease" ' \
        'OR role = "Gene Product Malfunction Associated With Disease")'
    return get_code_name_list_result(sql, [check_for_root(code)])


def search_diseases_is_stage(code):
    sql = 'SELECT DISTINCT rel.subject_code code, ncit.name name ' \
          'FROM ncit_relationships rel ' \
          'JOIN ncit ON rel.subject_code = ncit.code ' \
          'WHERE rel.object_code = ? ' \
          'AND role = "Disease Is Stage"'
    return get_code_name_list_result(sql, [check_for_root(code)])


def search_diseases_is_grade(code):
    sql = 'SELECT DISTINCT rel.subject_code code, ncit.name name ' \
          'FROM ncit_relationships rel ' \
          'JOIN ncit ON rel.subject_code = ncit.code ' \
          'WHERE rel.object_code = ? ' \
          'AND role = "Disease Is Grade"'
    return get_code_name_list_result(sql, [check_for_root(code)])


def get_subtree_codes(code):
    sql = 'WITH RECURSIVE ' \
          'subtree(x) AS (VALUES(?) ' \
          'UNION ' \
          'SELECT ncit.code FROM ncit, subtree ' \
          'WHERE ncit.parent_codes LIKE "%" || subtree.x ' \
          'OR ncit.parent_codes LIKE "%" || subtree.x || "|") ' \
          'SELECT ncit.code FROM ncit WHERE ncit.code IN subtree;'
    connection = sqlite3.connect('db/terminology.db')
    connection.row_factory = lambda cursor, row: row[0]
    results = []
    try:
        cursor = connection.cursor()
        cursor.execute(sql, [check_for_root(code)])
        results = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as e:
        logger.error("An error occurred:", e)
    return results


def get_child_codes(code):
    ccode = check_for_root(code)
    sql = 'select code, name from ncit where parent_codes like ? or parent_codes like ?'
    # parent codes are in a pipe (|) delimited list
    # just matching on the first term we get spurious substring matches
    # such as C8461 matching C84615
    querytokens = ['%' + ccode, '%' + ccode + '|%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def get_parent_codes(code):
    sql = 'select parent_codes from ncit where code = ?'
    parent_codes = get_single_string_result(sql, [code])
    results = []
    # parent codes are in a pipe (|) delimited list
    for parent_code in parent_codes.split('|'):
        sql = 'select code, name from ncit where code = ?'
        results.extend(get_code_name_list_result(sql, [parent_code]))
    return results


def get_name_for_code(domain, code):
    if domain == 'biomarkers':
        table = 'biomarkers'
    elif domain == 'diseases':
        table = 'neoplasm_core'
    else:
        table = 'ncit'

    sql = 'select name from ' + table + ' where code = ?'
    name = get_single_string_result(sql, [code])

    if name:
        return name

    sql = 'select name from ncit where code = ?'
    name = get_single_string_result(sql, [code])
    return name
