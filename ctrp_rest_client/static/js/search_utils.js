// load comma delimited list of concept codes from hidden string field and populate an UL
// will callback to retrieve names for the concept codes
// code_list_id - id of the text form field
// ul_list_id - id of the ul list
function refresh_list_from_hidden(code_list_id, ul_list_id) {

    var code_list = '#' + code_list_id;
    var ul_list = '#' + ul_list_id;
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

    $('#' + code).remove();
    var codes = $('#' + list_id).val().split(', ');
    var pos = codes.indexOf(code);
    codes.splice(pos, 1);
    $('#' + list_id).val(codes.join(", "));
};


// generates link for selected code and name
// to be appended in the ul
function create_li(code, name, code_list_id) {

    return '<li id="' + code + '">'
    + '<a href="#" onclick="rm_term(\'' + code + '\', \'' + code_list_id + '\');">remove</a>'
    + '&nbsp; ' + name + '</li>';
};