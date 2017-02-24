// add pound symbol for jquery element id addressing
function tag_id(id_name) {
    return '#' + id_name;
}

// load comma delimited list of concept codes from hidden string field and populate an UL
// will callback to retrieve names for the concept codes
// code_list_id - id of the text form field
// ul_list_id - id of the ul list
function refresh_list_from_hidden(code_list_id, ul_list_id) {

    var code_list = tag_id(code_list_id);
    var ul_list = tag_id(ul_list_id);
    var codes = $(code_list).val().split(', ');
    if (codes[0] == "") codes = [];
    $.each(codes, function (i, code) {

        $.get('get_name_for_ncit_code?code=' + code + '&dom=' + ul_list_id, function(data) {
            var name = data.replace('_', ' ');
            $(ul_list).append(create_li(code, name, code_list_id));
        });
    });
};


// remove term from comma separated list in text field
function rm_term(code, list_id) {

    $(tag_id(code)).remove();
    var codes = $('#' + list_id).val().split(', ');
    var pos = codes.indexOf(code);
    codes.splice(pos, 1);
    $(tag_id(list_id)).val(codes.join(", "));
};


// generates link for selected code and name
// to be appended in the ul
function create_li(code, name, code_list_id) {

    return '<li id="' + code + '">'
    + '<a href="#" onclick="rm_term(\'' + code + '\', \'' + code_list_id + '\');">remove</a>'
    + '&nbsp; ' + name + '</li>';
};

// updates hidden code list and visible list of names fore
// terms selected in typeahead field search
function update_typeahead(item, code_list_id, ul_list_id) {

    var code_list = tag_id(code_list_id);
    var ul_list = tag_id(ul_list_id);
    var code = map[item].data;

    if(!$(code_list).val().includes(code)) {
        $(code_list).val( $.grep([$(code_list).val(), code], Boolean).join(", ") );
        $(ul_list).append( create_li(code, item, code_list_id) );
    }
};
