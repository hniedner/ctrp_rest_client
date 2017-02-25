// add pound symbol for jquery element id addressing
function tag_id(id_name) {

    return '#' + id_name;
};

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
        if (name != '') {
            var code = codes[i];
            $(fields.ul_list).append(create_li(code, name, dom));
        }
    });
};

// wrapper to call the remove_term for both names and code hidden fields
function rm_term(code, name, dom) {

    var fields = get_fields(dom);
    // remove ul list item
    $(tag_id(code)).remove();
    // remove name from hidden form field
    remove_term(name, fields.name_list);
    // remove code from hidden form field
    remove_term(code, fields.code_list);
};

// remove term from comma separated list in text field
function remove_term(term, list_id) {

    var hidden_field_value = $(list_id).val();
    var terms = hidden_field_value.split(', ');
    var pos = terms.indexOf(term);
    terms.splice(pos, 1);
    $(list_id).val(terms.join(", "));
};

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function expand_term(code, dom) {

    $.get('expand_ncit_code?code=' + code, function (data) {
        data.forEach(function(entry) {

            var code = entry.code;
            var name = entry.name.replace(/_/g,' ');
            update_selections(code, name, dom);
        });
    });
};


// generates link for selected code and name
// to be appended in the ul
function create_li(code, name, dom) {

    return '<li id="' + code + '">'
    + '<a href="#" onclick="rm_term(\'' + code + '\', \'' + name + '\', \'' + dom + '\');">remove</a>'
    + '&nbsp; ' + '<a href="#" onclick="expand_term(\'' + code + '\', \'' + dom + '\');">expand</a>'
    + '&nbsp; ' + name + '</li>';
};

// update the hidden fields for codes and names
// and the unordered list for selected terms
function update_selections(code, name, dom) {

    var fields = get_fields(dom);

    if(!$(fields.code_list).val().includes(code)) {
        $(fields.name_list).val( $.grep([$(fields.name_list).val(), name], Boolean).join(", ") );
        $(fields.code_list).val( $.grep([$(fields.code_list).val(), code], Boolean).join(", ") );
        $(fields.ul_list).append( create_li(code, name, dom) );
    };
};