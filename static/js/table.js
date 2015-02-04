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
        },
        {
            name: "gender",
            label: "Пол",
            datatype: "string",
            editable: true
        },
        {
            name: "birthdate",
            label: "Дата рождения",
            datatype: "string",
            editable: true
        },
        {
            name: "address",
            label: "Адрес",
            datatype: "string",
            editable: true
        },
        {
            name: "email",
            label: "E-Mail",
            datatype: "email",
            editable: true
        },
        {
            name: "phone",
            label: "Телефон",
            datatype: "string",
            editable: true
        },
    ];
}

$(document).ready(function () {
    var editableGrid = new EditableGrid("Address Book");
    var metadata = prepareMeta();

    function updateTable() {
        $.ajax({
            url: '/data/',
            type: 'GET',
            data: {}
        }).done(function (data) {
            var phone, date;

            for (var I in data) {
                phone = data[I].values.phone;
                data[I].values.phone = '8(' + phone.substr(0, 3) + ')' + phone.substring(3);
            }

            editableGrid.load({"metadata": metadata, "data": data});
            editableGrid.renderGrid("tablecontent", "grid");
        }).fail(function (jqXHR, textStatus) {
            alert(textStatus);
        });
    }

    updateTable();
    $('#filter').change(function () {
        var filter = $('#filter').val();
        editableGrid.filter(filter);
    });

    function addPerson(event) {
        event.preventDefault();
        var form = $(this);

        // validate

        var url = form.attr('action');
        var inputs = $('#add-person-form :input');

        var params = {};
        inputs.each(function() {
            if (this.type != 'radio' || this.checked)
                params[this.name] = $(this).val();
        });

        $.ajax({
            url: url,
            type: 'POST',
            data: params
        }).done(function (response) {
            alert(response);
        }).fail(function (jqXHR, textStatus) {
            alert(textStatus);
        });
    }

    var addForm = $('#add-person-form');
    $('#save-btn').click(function () {
        addForm.trigger("submit");
    });
    addForm.submit(addPerson);

    function updateField() {
        var params = {id: 0, field: 'fullname', new_value: 'Кисленко Максим'};

        $.ajax({
            url: '/update/',
            type: 'POST',
            data: params
        }).done(function (response) {
            alert(response);
        }).fail(function (jqXHR, textStatus) {
            alert(textStatus);
        });
    }

    for (var I = 0; I < editableGrid.getColumnCount(); I++) {
        editableGrid.setCellEditor(I, updateField);
    }
});