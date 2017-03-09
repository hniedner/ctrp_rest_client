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

function _do_code_callback(code, dom, url, reverse) {

    $.get(url + code, function (data) {
        data.forEach(function(entry) {
            var code = entry.code;
            var name = entry.name.replace(/_/g,' ');
            if (reverse) {
                rm_term(code, name, dom);
            } else {
                add_term(code, name, dom);
            }
        });
    });
}

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function add_child_terms(code, dom) {
    _do_code_callback(code, dom, 'get_child_codes?code=', false);
}

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function rm_child_terms(code, dom) {
    _do_code_callback(code, dom, 'get_child_codes?code=', true);
}

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function add_parent_terms(code, dom) {
    _do_code_callback(code, dom, 'get_parent_codes?code=', false);
}

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function rm_parent_terms(code, dom) {
    _do_code_callback(code, dom, 'get_parent_codes?code=', true);
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

    if(!$(fields.code_list).val().includes(code)) {
        add_item_to_comma_delimited_list(fields.name_list, name);
        add_item_to_comma_delimited_list(fields.code_list, code);
        $(fields.ul_list).append( create_li(code, name, dom) );
    }
}

// split the comma-delimited string into array
// add item to list if it doesn't already exist in the list
// join it back together and replace the value
function add_item_to_comma_delimited_list(field_name, item) {

    $(field_name).val( $.grep([$(field_name).val(), item], Boolean).join(", ") );
}



function update_tree(code, item, dom) {
    var tree = $('#jstree').jstree(true);
    var root = tree.get_node('root');
    var node = build_jstree_node(code, item, 'root');
    add_jstree_node(root, node, tree);
}

function get_code_for_id(node_id) {
    var codes = node_id.split('*');
    return codes[codes.length-1];
}

function get_id_for_code(parent_code, code) {
    return parent_code ? parent_code + '*' + code : code;
}

function get_icon_for_code(code) {
    return (code === 'root') ? 'glyphicon glyphicon-info-sign' : 'glyphicon glyphicon-check';
}

function build_jstree_node(code, name, parent_id) {
    var id;
    if (parent_id) {
        var parent_code = get_code_for_id(parent_id);
        id = get_id_for_code(parent_code, code);
    } else {
        id = code;
    }
    var node = {
        'id': id,
        'text': name.replace(/_/g,' '),
        'icon': get_icon_for_code(code),
        'state': { 'opened' : true, 'selected' : false }
    };
    return node;
}

function add_jstree_node(parent, node, tree) {
    if(tree.get_node(node)) {
        return node.id;
    }
    var position = 'last';
    function callback(){ }
    function is_loaded(){ }
    return tree.create_node(parent, node, position, callback, is_loaded);
}

function add_children(parent, tree, node_ids_to_recurse) {
    parent.state.opened = true;
    parent.state.selected = true;
    $.get('/get_child_codes?code=' + get_code_for_id(parent.id), function (data) {
        data.forEach(function (item) {
            var node = build_jstree_node(item.code, item.name, parent.id);
            if(tree.get_node(node)) {
                if(tree.is_leaf(node) === false) {
                    node_ids_to_recurse = node_ids_to_recurse ? node_ids_to_recurse : [];
                    node_ids_to_recurse.push(node.id);
                }
                tree.delete_node(node);
            }
            var new_id = add_jstree_node(parent, node, tree);
            if(node_ids_to_recurse && node_ids_to_recurse.includes(new_id)) {
                tree.select_node(node);
                add_children(node, tree);
                node_ids_to_recurse.pop(new_id);
            }
        });
    });
}

function remove_children(parent, tree) {
    parent.state.opened = false;
    $.get('/get_child_codes?code=' + get_code_for_id(parent.id), function (data) {
        data.forEach(function(item) {
            var parent_code = get_code_for_id(parent.id);
            var id = get_id_for_code(parent_code, item.code);
            var node = tree.get_node(id);
            if(node) {
                tree.delete_node(node);
            }
        });
    });
}

function add_parents(child, tree) {
    var current_parent_id = tree.get_parent(child);
    var current_parent = tree.get_node(current_parent_id);
    var grandparent = ('root' === current_parent_id) ? current_parent : tree.get_node(tree.get_parent(current_parent));
    var child_code = get_code_for_id(child.id);
    $.get('/get_parent_codes?code=' + child_code, function (data) {
        data.forEach(function(item) {
            var parent_code = item.code;
            var parent = build_jstree_node(parent_code, item.name, grandparent.id);
            if (tree.get_node(parent) === false) {
                add_jstree_node(grandparent, parent, tree);
                add_children(parent, tree, [get_id_for_code(parent_code, child_code)]);
                // we dispose the child nodes
                if ('root' === current_parent_id) {
                    tree.delete_node(child);
                }
            }
        });
    });
}

function remove_parents(child, tree) {
    var parent_id = tree.get_parent(child);
    var parent = tree.get_node(parent_id);
    if(parent && parent !== tree.get_node('root')) {
        tree.delete_node(parent);
    }
}

function get_jstree_context_menu() {
    return {
        "items": function($node) {
            var tree = $("#jstree").jstree(true);
            return {
                "Remove": {
                    "separator_before": false,
                    "separator_after": false,
                    "icon": 'glyphicon glyphicon-minus',
                    "label": "Remove",
                    "action": function (obj) {
                        if ($node !== tree.get_node('root')) {
                            tree.delete_node($node);
                        }
                    }
                },
                "AddChildren": {
                    "separator_before": false,
                    "separator_after": false,
                    "icon": 'glyphicon glyphicon-plus',
                    "label": "Add child concepts",
                    "action": function (obj) {
                        add_children($node, tree);
                    }
                },
                "RemoveChildren": {
                    "separator_before": false,
                    "separator_after": false,
                    "icon": 'glyphicon glyphicon-minus',
                    "label": "Remove child concepts",
                    "action": function (obj) {
                        remove_children($node, tree);
                    }
                },
                "AddParent": {
                    "separator_before": false,
                    "separator_after": false,
                    "icon": 'glyphicon glyphicon-plus',
                    "label": "Add parent concepts",
                    "action": function (obj) {
                        add_parents($node, tree);
                    }
                },
                "RemoveParents": {
                    "separator_before": false,
                    "separator_after": false,
                    "icon": 'glyphicon glyphicon-minus',
                    "label": "Remove parent concepts",
                    "action": function (obj) {
                        remove_parents($node, tree);
                    }
                }
            };
        }
    }
}