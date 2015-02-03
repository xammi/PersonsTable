/**
 * Created by max on 03.02.15.
 */

function prepareMeta() {
    return [
        {
            name: "fullname",
            label: "ФИО",
            datatype: "string",
            editable: true
        },{
            name: "gender",
            label: "Пол",
            datatype: "string",
            editable: true
        },{
            name: "birthdate",
            label: "Дата рождения",
            datatype: "string",
            editable: true
        },{
            name: "address",
            label: "Адрес",
            datatype: "string",
            editable: true
        },{
            name: "email",
            label: "E-Mail",
            datatype: "string",
            editable: true
        },{
            name: "phone",
            label: "Телефон",
            datatype: "string",
            editable: true
        },
    ];
}

function fetchData(params, callback) {
    $.ajax({
        url: '/data/',
        type: 'GET',
        data: params
    }).done(function (data) {
        callback(data);
    }).fail(function (jqXHR, textStatus) {
        alert(textStatus);
    });
}

function updateTable() {
    var editableGrid = new EditableGrid("Address Book");
    var metadata = prepareMeta();

    fetchData({}, function (data) {
        editableGrid.load({"metadata": metadata, "data": data});
        editableGrid.renderGrid("tablecontent", "grid");
    });
}

$(document).ready(function () {
    updateTable();
    $('#updater').click(updateTable);
});