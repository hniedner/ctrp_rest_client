"use strict";

// add pound symbol for jquery element id addressing
function tag_id(id_name) {

    return '#' + id_name;
}

// translate domain (search category such as disease, biomarker, etc.)
// into standardized field ids following the convention:
// disease ->
//      disease_names -> for hidden field holding the concept names as comma delimited string
//      disease_codes -> for hidden field holding the concept codes as comma delimited string
//      diseases      -> for unordered list of selected concept names
function get_fields(dom) {

    return {
        'name_list': tag_id(dom + '_names'),
        'code_list': tag_id(dom + '_codes'),
        'ul_list': tag_id(dom + 's')
    }
}

// load comma delimited list of concept codes from hidden string field and populate an UL
// will callback to retrieve names for the concept codes
// code_list_id - id of the text form field
// ul_list_id - id of the ul list
function refresh_ul_list_from_hidden(dom) {

    var fields = get_fields(dom);
    var names = $(fields.name_list).val().split(', ');
    var codes = $(fields.code_list).val().split(', ');

    $.each(names, function (i, name) {
        if (name !== '') {
            var code = codes[i];
            $(fields.ul_list).append(create_li(code, name, dom));
        }
    });
}

// wrapper to call the remove_term for both names and code hidden fields
function rm_term(code, name, dom) {

    var fields = get_fields(dom);
    // remove ul list item
    $(tag_id(code)).remove();
    // remove name from hidden form field
    remove_term(name, fields.name_list);
    // remove code from hidden form field
    remove_term(code, fields.code_list);
}

// remove term from comma separated list in text field
function remove_term(term, list_id) {

    var hidden_field_value = $(list_id).val();
    var terms = hidden_field_value.split(', ');
    var pos = terms.indexOf(term);
    terms.splice(pos, 1);
    $(list_id).val(terms.join(", "));
}

// execute ajax callback, loop through server response
// execute process_entry function for each return object (name code).
function _do_code_callback(dom, url, process_entry) {

    $.get(url, function (data) {
        data.forEach(function (entry) {
            var code = entry.code;
            var name = entry.name.replace(/_/g, ' ');
            process_entry(code, name, dom);
        });
    });
}

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function add_child_terms(code, dom) {
    _do_code_callback(dom, 'get_child_codes?code=' + code + '&dom=' + dom, add_term);
}

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function rm_child_terms(code, dom) {
    _do_code_callback(dom, 'get_child_codes?code=' + code + '&dom=' + dom, rm_term);
}

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function add_parent_terms(code, dom) {
    _do_code_callback(dom, 'get_parent_codes?code=' + code + '&dom=' + dom, add_term);
}

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function rm_parent_terms(code, dom) {
    _do_code_callback(dom, 'get_parent_codes?code=' + code, rm_term);
}

// generates link for selected code and name
// to be appended in the ul
function create_li(code, name, dom) {

    return '<li id="' + code + '">'
        + '<a href="#" onclick="rm_term(\'' + code + '\', \'' + name + '\', \'' + dom + '\');">remove</a>'
        + '&nbsp;|&nbsp;<a href="#" onclick="add_child_terms(\'' + code + '\', \'' + dom + '\');">add child terms</a>'
        + '&nbsp;|&nbsp;<a href="#" onclick="rm_child_terms(\'' + code + '\', \'' + dom + '\');">remove child terms</a>'
        + '&nbsp;|&nbsp;<a href="#" onclick="add_parent_terms(\'' + code + '\', \'' + dom + '\');">add parent terms</a>'
        + '&nbsp;|&nbsp;<a href="#" onclick="rm_parent_terms(\'' + code + '\', \'' + dom + '\');">remove parent terms</a>'
        + '&nbsp;|&nbsp;' + name + '</li>';
}

// update the hidden fields for codes and names
// and the unordered list for selected terms
function add_term(code, name, dom) {

    var fields = get_fields(dom);

    if (!$(fields.code_list).val().includes(code)) {
        add_item_to_comma_delimited_list(fields.name_list, name);
        add_item_to_comma_delimited_list(fields.code_list, code);
        $(fields.ul_list).append(create_li(code, name, dom));
    }
}

// split the comma-delimited string into array
// add item to list if it doesn't already exist in the list
// join it back together and replace the value
function add_item_to_comma_delimited_list(field_name, item) {
    $(field_name).val($.grep([$(field_name).val(), item], Boolean).join(", "));
}


function update_tree(code, item) {
    var tree = $('#jstree').jstree(true);
    tree.settings.core.data = build_jstree_node(code, item);
    tree.refresh();
}

function get_code_for_id(node_id) {
    var codes = node_id.split('*');
    return codes[codes.length - 1];
}

function get_id_for_code(parent_code, code) {
    return parent_code ? parent_code + '*' + code : code;
}

function build_jstree_node(code, name, parent_id) {
    var id;
    if (parent_id) {
        var parent_code = get_code_for_id(parent_id);
        id = get_id_for_code(parent_code, code);
    } else {
        id = code;
    }
    return {
        'id': id,
        'text': name.replace(/_/g, ' '),
        'state': {'opened': false, 'selected': false}
    };
}

function add_jstree_node(parent, node, tree) {
    if (tree.get_node(node)) {
        return node.id;
    }
    var position = 'last';

    function callback() {
    }

    function is_loaded() {
    }

    return tree.create_node(parent, node, position, callback, is_loaded);
}

function add_children(parent, tree, node_ids_to_recurse) {
    parent.state.opened = true;
    parent.state.selected = true;
    $.get('/get_child_codes', {code: get_code_for_id(parent.id), dom: dom}, function (data) {
        data.forEach(function (item) {
            var node = build_jstree_node(item.code, item.name, parent.id);
            if (tree.get_node(node)) {
                if (tree.is_leaf(node) === false) {
                    node_ids_to_recurse = node_ids_to_recurse ? node_ids_to_recurse : [];
                    node_ids_to_recurse.push(node.id);
                }
                tree.delete_node(node);
            }
            var new_id = add_jstree_node(parent, node, tree);
            if (node_ids_to_recurse && node_ids_to_recurse.includes(new_id)) {
                tree.select_node(node);
                add_children(node, tree);
                node_ids_to_recurse.pop(new_id);
            }
        });
    });
}

function remove_children(parent, tree) {
    parent.state.opened = false;
    var children = tree.get_children_dom(parent);
    children.each(
        function (index, child) {
            tree.delete_node(child);
        }
    );
}

function get_callback_url(dom) {
    var url = '';
    if ('disease' === dom) {
        url = 'search_diseases?q=';
    } else if ('finding' === dom) {
        url = 'search_findings?q=';
    } else if ('diagnostic' === dom) {
        url = 'search_diagnostic_test?q=';
    } else if ('test' === dom) {
        url = 'search_lab_test?q=';
    } else if ('drug' === dom) {
        url = 'search_drugs?q=';
    } else if ('procedure' === dom) {
        url = 'search_therapies?q=';
    } else if ('biomarker' === dom) {
        url = 'search_biomarkers?q=';
    } else if ('anatomicsite' === dom) {
        url = 'search_anatomicsites?q=';
    } else if ('tissue' === dom) {
        url = 'search_tissues?q=';
    }
    return url;
}

function search_selected_nodes(dom, datatable, node_ids) {
    $("[name='results_length']").val(10); // reset the row number to 10
    datatable.search(JSON.stringify({})).draw(); // reset the datatable to all trials
    // reset the total record counter and display temporary spinner
    var records_total = $("#records_total");
    records_total.text('');
    records_total.prepend('<img style="width:2%;" src="static/img/spinner.gif"/>');
    var codes = [];
    for (var i = 0; i < node_ids.length; i++) {
        var code = get_code_for_id(node_ids[i]);
        codes.push(code);
    }
    console.log(codes);

    var search_params = {};

    if ('disease' === dom) {
        search_params['diseases.nci_thesaurus_concept_id'] = codes;
        datatable.search(JSON.stringify(search_params)).draw();
    } else if ('biomarker' === dom) {
        search_params['biomarkers.nci_thesaurus_concept_id'] = codes;
        datatable.search(JSON.stringify(search_params)).draw();
    }
}

function select_subtree(node, dom, datatable) {
    var code = get_code_for_id(node.id);
    $.get('get_subtree_codes', {code: code, dom: dom}, function (codes) {
        codes.push(code); // add in the parent concept that was selected
        if ('disease' === dom) {
            search_params['diseases.nci_thesaurus_concept_id'] = codes;
        } else if ('biomarker' === dom) {
            search_params['biomarkers.nci_thesaurus_concept_id'] = codes;
        }
        datatable.search(JSON.stringify(search_params)).draw();
    });
}

function _build_jstree_context_menu_item(label, action) {
    return {
        "separator_before": false,
        "separator_after": false,
        "icon": 'glyphicon glyphicon-minus',
        "label": label,
        "action": action
    }
}

// timeout to avoid single click jstree event trigger on double click
var is_enabled = true;
function timer() {
    is_enabled = false;
    setTimeout(function () {
        is_enabled = true;
    }, 250); // 250 ms seems to be the sweet spot for me wrt double click speed
}

function _toggle_leafnode(selector, leafnode_id) {
    var tree = $(selector).jstree(true);
    var node = tree.get_node(leafnode_id);
    if (tree.is_leaf(node)) {
        add_children(node, tree, dom);
    } else {
        remove_children(node, tree);
    }
}

function build_jstree(selector) {
    return $(selector).jstree({
        plugins: ['contextmenu', 'dnd', 'search', 'sort', 'checkbox'],
        core: {
            check_callback: true,
            data: [],
            themes: {"icons": false}
        },
        checkbox: {
            three_state: false,
            cascade: 'undetermined',
            whole_node: false
        },
        search: {
            case_insensitive: true,
            show_only_matches: true
        },
        contextmenu: get_jstree_context_menu(selector)

    }).on('dblclick', '.jstree-anchor', function () {
        _toggle_leafnode(selector, this);

    }).on('click', '.jstree-anchor', function () {
        // avoid triggering the single click event on the doubleclick
        if (is_enabled) {
            search_selected_nodes(dom, datatable, $(selector).jstree(true).get_checked());
            timer();
        }
    });
}

function get_jstree_context_menu(selector) {
    return {
        "items": function (node) {
            return {
                "SelectChildren": _build_jstree_context_menu_item(
                    "Select Child Concepts",
                    function check_children() {
                        _toggle_children_checkboxes(selector, node, true);
                    }
                ),

                "DeSelectChildren": _build_jstree_context_menu_item(
                    "Deselect Child Concepts",
                    function check_children() {
                        _toggle_children_checkboxes(selector, node, false);
                    }
                ),

                "Expand": _build_jstree_context_menu_item(
                    "Expand Tree",
                    function check_children() {
                        $(selector).jstree(true).open_all();
                    }
                ),

                "Collapse": _build_jstree_context_menu_item(
                    "Collapse Tree",
                    function check_children() {
                        $(selector).jstree(true).close_all();
                    }
                )
            }
        }
    }
}

function _toggle_children_checkboxes(selector, node, check) {
    var tree = $(selector).jstree(true);

    // add children before trying to check them
    if (tree.is_leaf(node)) {
        add_children(node, tree, dom);
    }

    setTimeout(function () {

        // open the node and expose the children
        if (tree.is_closed(node)) {
            tree.open_node(node);
        }

        // if selecting the child nodes deselect parent
        // if deselecting the child nodes select parent
        if (check) {
            tree.uncheck_node(node);
        } else {
            tree.check_node(node);
        }

        // enable the checkboxes for all children
        var children = tree.get_children_dom(node);
        // avoid asynchronous loop to make sure all nodes are checked before search commences
        for(var i = 0; i < children.length; i++){
            var child = children[i];
            if (check) {
                console.log(child);
                tree.check_node(child); // using the children directly only selects first node
            } else {
                tree.uncheck_node(child);
            }
        }
        search_selected_nodes(dom, datatable,tree.get_checked());
    }, 500);
}
