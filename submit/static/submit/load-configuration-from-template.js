if (!$) { var $ = django.jQuery; }

var submit_receiver_configuration_templates;

function update_textarea() {
    var selected_template = $("#id_receiver_template").val();
    if (selected_template in submit_receiver_configuration_templates) {
        var template_json = submit_receiver_configuration_templates[selected_template];
        $("#id_configuration").val(JSON.stringify(template_json, null, 2));
    }
}

$(document).ready(function() {
    var configuration_textarea = $("#id_configuration");

    if (configuration_textarea.val() != "{}") {
        var configuration_json = JSON.parse(configuration_textarea.val());
        configuration_textarea.val(JSON.stringify(configuration_json, null, 2));
    }

    $.getJSON("/submit/ajax/get_receiver_templates/", function (data) {
        submit_receiver_configuration_templates = data;
        if ($("#id_configuration").val() == "{}") {
            update_textarea();
        }
    });

    $("#id_receiver_template").change(update_textarea);
});
