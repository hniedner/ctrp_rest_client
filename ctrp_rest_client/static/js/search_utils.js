// add pound symbol for jquery element id addressing
function tag_id(id_name) {

    return '#' + id_name;
};

// load comma delimited list of concept codes from hidden string field and populate an UL
// will callback to retrieve names for the concept codes
// code_list_id - id of the text form field
// ul_list_id - id of the ul list
function refresh_ul_list_from_hidden(dom) {

    var code_list_id = dom + '_codes';
    var name_list_id = dom + '_names';
    var ul_list_id = dom + 's';
    var names = $(tag_id(name_list_id)).val().split(', ');
    var codes = $(tag_id(code_list_id)).val().split(', ');

    $.each(names, function (i, name) {
        if (name != '') {
            var code = codes[i];
            $(tag_id(ul_list_id)).append(create_li(code, name, dom));
        }
    });
};

// wrapper to call the remove_term for both names and code hidden fields
function rm_term(code, name, dom) {

    var name_list_id = dom + '_names';
    var code_list_id = dom + '_codes';
    // remove ul list item
    $(tag_id(code)).remove();
    // remove name from hidden form field
    remove_term(name, name_list_id);
    // remove code from hidden form field
    remove_term(code, code_list_id);
};

// remove term from comma separated list in text field
function remove_term(term, list_id) {

    var hidden_field_value = $(tag_id(list_id)).val();
    var terms = hidden_field_value.split(', ');
    var pos = terms.indexOf(term);
    terms.splice(pos, 1);
    $(tag_id(list_id)).val(terms.join(", "));
};

// code is nci thesaurus concept id
// dom is domain either biomarker or disease (or other in the future)
function expand_term(code, dom) {

    var name_list_id = dom + '_names';
    var code_list_id = dom + '_codes';
    var ul_list_id = dom + 's';

    $.get('expand_ncit_code?code=' + code, function (data) {
        data.forEach(function(entry) {

            var code = entry.data;
            var name = entry.value.replace('_',' ');

            // TODO: creates dublicate entries - Fix!
            $(tag_id(code_list_id)).val(
                $.grep([$(tag_id(code_list_id)).val(), code], Boolean).join(", ") );

            $(tag_id(name_list_id)).val(
                $.grep([$(tag_id(name_list_id)).val(), name], Boolean).join(", ") );

            $(tag_id(ul_list_id)).append( create_li(entry.data, name, dom) );
        });
    });
}


// generates link for selected code and name
// to be appended in the ul
function create_li(code, name, dom) {

    return '<li id="' + code + '">'
    + '<a href="#" onclick="rm_term(\'' + code + '\', \'' + name + '\', \'' + dom + '\');">remove</a>'
    + '&nbsp; ' + '<a href="#" onclick="expand_term(\'' + code + '\', \'' + dom + '\');">expand</a>'
    + '&nbsp; ' + name + '</li>';
};

// updates hidden code list and visible list of names fore
// terms selected in typeahead field search
function update_typeahead(item, dom) {

    var name_list_id = dom + '_names';
    var code_list_id = dom + '_codes';
    var ul_list_id = dom + 's';
    var name_list = tag_id(name_list_id);
    var code_list = tag_id(code_list_id);
    var ul_list = tag_id(ul_list_id);
    var code = map[item].data;

    if(!$(code_list).val().includes(code)) {

        $(name_list).val( $.grep([$(name_list).val(), item], Boolean).join(", ") );

        $(code_list).val( $.grep([$(code_list).val(), code], Boolean).join(", ") );

        $(ul_list).append( create_li(code, item, dom) );
    }
};
