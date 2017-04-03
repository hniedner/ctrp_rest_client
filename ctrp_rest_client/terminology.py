import logging
import sqlite3

# create logger
logger = logging.getLogger('terminology')


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


def search_anatomicsite_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where semantic_type = "Body Part, Organ, or Organ Component" ' \
          'and (name like ? or synonyms like ?)'
    querytokens = ['%' + query + '%', '%' + query + '%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def search_tissue_by_substring(query):
    sql = 'select code, name from ncit ' \
          'where semantic_type = "Tissue" ' \
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
    sql = 'select ncit.code, ncit.name from biomarkers ' \
          'JOIN ncit ON biomarkers.code = ncit.code ' \
          'where ncit.name like ? or ncit.synonyms like ?'
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
    results = get_code_name_list_result(sql, [check_for_root(code, 'anantomicsite')])
    return results


def search_diseases_associated_with_finding(code):
    sql = 'SELECT DISTINCT rel.subject_code code, ncit.name name ' \
          'FROM ncit_relationships rel ' \
          'JOIN ncit ON rel.subject_code = ncit.code ' \
          'WHERE rel.object_code = ? ' \
          'AND role = "Disease Has Finding"'
    return get_code_name_list_result(sql, [check_for_root(code, 'finding')])


def search_diseases_associated_with_gene(code):
    sql = 'select rel.subject_code, ncit.name ' \
        'FROM ncit_relationships rel ' \
        'JOIN ncit ON ncit.code = rel.subject_code ' \
        'WHERE rel.object_code = ? ' \
        'AND (role = "Gene Associated With Disease" ' \
        'OR role = "Gene Involved In Pathogenesis Of Disease" ' \
        'OR role = "Gene Product Malfunction Associated With Disease")'
    return get_code_name_list_result(sql, [check_for_root(code, 'gene')])


def search_diseases_is_stage(code):
    sql = 'SELECT DISTINCT rel.subject_code code, ncit.name name ' \
          'FROM ncit_relationships rel ' \
          'JOIN ncit ON rel.subject_code = ncit.code ' \
          'WHERE rel.object_code = ? ' \
          'AND role = "Disease Is Stage"'
    return get_code_name_list_result(sql, [check_for_root(code, 'disease')])


def search_diseases_is_grade(code):
    sql = 'SELECT DISTINCT rel.subject_code code, ncit.name name ' \
          'FROM ncit_relationships rel ' \
          'JOIN ncit ON rel.subject_code = ncit.code ' \
          'WHERE rel.object_code = ? ' \
          'AND role = "Disease Is Grade"'
    return get_code_name_list_result(sql, [check_for_root(code, 'disease')])


def get_subtree_codes(code, dom):
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
        cursor.execute(sql, [check_for_root(code, dom)])
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
    sql = 'select code, name from ncit where parent_codes like ? or parent_codes like ?'
    querytokens = ['%' + ccode, '%' + ccode + '|%']
    results = get_code_name_list_result(sql, querytokens)
    return results


def get_parent_codes(code, dom):
    ccode = check_for_root(code, dom)
    sql = 'select parent_codes from ncit where code = ?'
    parent_codes = get_single_string_result(sql, [ccode])
    results = []
    # parent codes are in a pipe (|) delimited list
    for parent_code in parent_codes.split('|'):
        sql = 'select code, name from ncit where code = ?'
        results.extend(get_code_name_list_result(sql, [parent_code]))
    return results


def get_root_concept(dom):
    root_concepts = {
        'disease': {'name': 'Neoplasm', 'code': 'C3262'},
        'finding': {'name': 'Finding', 'code': 'C3367'},
        'diagnostic': {'name': 'Diagnostic Procedure', 'code': 'C18020'},
        'test': {'name': 'Laboratory Procedure', 'code': 'C25294'},
        'procedure': {'name': 'Therapeutic Procedure', 'code': 'C3262'},
        'anatomicsite': {'name': 'Anatomic Site', 'code': 'C13717'},
        'drug': {'name': 'Pharmacologic Substance', 'code': 'C1909'}
    }
    return root_concepts[dom] if dom in root_concepts else {'name': 'Disease, Disorder or Finding', 'code': 'C7057'}
