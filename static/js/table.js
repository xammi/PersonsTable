/**
 * Created by max on 03.02.15.
 */


var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

//--------------------------------------------------------------------------------------------
var Validators = {
    fullname: function (value) {
        return /[А-Я|A-Z][а-я|a-z]+ [А-Я|A-Z][а-я|a-z]+/.test(value);
    },
    birthdate: function (value) {
        return /\d{4}-\d{2}-\d{2}/.test(value);
    },
    gender: function (value) {
        return /[M|F]/.test(value);
    },
    address: function (value) {
        return /г. [А-Я][а-я]+, ул. [А-Я][а-я]+, д. \d+/.test(value);
    },
    email: function (value) {
        return /\w+@\w+\.[a-z]+/.test(value);
    },
    phone: function (value) {
        return /8\d{10}/.test(value);
    }
};


function validate(params) {

    function apply(field) {
        var value = params[field];
        var validator = Validators[field];

        if (! validator(value)) {
            showAlert('error', 'form-alerts', 'Invalid field: ' + field);
            return false;
        }
        return true;
    }

    for (var I in Validators)
        if (Validators.hasOwnProperty(I))
            if (! apply(I)) return false;

    return true;
}

function writeAlert(kind, blockId, text) {
    var item;
    var block = $('#' + blockId);
    if (kind === 'success')
        item = block.children('.alert-success');
    else if (kind === 'error')
        item = block.children('.alert-danger');

    item.html(item.html() + '\n\n' + text);
    return item;
}

function showAlert(kind, blockId, text) {
    var item = writeAlert(kind, blockId, text);
    item.fadeIn('slow').delay(10000).fadeOut('slow', function () {
        item.html('');
    });
}

function extractErrors(errors, action) {
    for (var field in errors) {
        if (errors.hasOwnProperty(field)) {
            var fieldErrors = errors[field];

            for (var error in fieldErrors) {
                if (fieldErrors.hasOwnProperty(error))
                    action(fieldErrors[error]);
            }
        }
    }
}
//-------------------------------------------------------------------------------------------------

function prepareMeta() {
    return [
        {
            name: "fullname",
            label: "ФИО",
            datatype: "string",
            editable: true,
            cellValidators: [new CellValidator({isValid: Validators.fullname})]
        },
        {
            name: "gender",
            label: "Пол",
            datatype: "string",
            editable: true,
            cellValidators: [new CellValidator({isValid: Validators.gender})]
        },
        {
            name: "birthdate",
            label: "Дата рождения",
            datatype: "string",
            editable: true,
            cellValidators: [new CellValidator({isValid: Validators.birthdate})]
        },
        {
            name: "address",
            label: "Адрес",
            datatype: "string",
            editable: true,
            cellValidators: [new CellValidator({isValid: Validators.address})]
        },
        {
            name: "email",
            label: "E-Mail",
            datatype: "email",
            editable: true,
            cellValidators: [new CellValidator({isValid: Validators.email})]
        },
        {
            name: "phone",
            label: "Телефон",
            datatype: "string",
            editable: true,
            cellValidators: [new CellValidator({isValid: Validators.phone})]
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
        }).done(function (response) {
            if (response.status == 'OK') {
                var phone, date;
                var data = response.data;

                for (var I in data) {
                    phone = data[I].values.phone;
                    data[I].values.phone = '8(' + phone.substr(0, 3) + ')' + phone.substring(3);
                }

                editableGrid.load({"metadata": metadata, "data": data});
                editableGrid.renderGrid("tablecontent", "grid");
            }
        }).fail(function (jqXHR, textStatus) {
            showAlert('error', 'gen-alerts', 'Unable to update. Please, check the connection.');
        });
    }

    updateTable();
    $('#updater').click(updateTable);
    $('#filter').change(function () {
        var filter = $('#filter').val();
        editableGrid.filter(filter);
    });

    function addPerson(event) {
        event.preventDefault();

        var form = $(this);
        var url = form.attr('action');
        var inputs = $('#add-person-form :input');

        var params = {};
        inputs.each(function() {
            if (this.type != 'radio' || this.checked)
                params[this.name] = $(this).val();
        });

        if (! validate(params))
            return false;

        $.ajax({
            url: url,
            type: 'POST',
            data: params
        }).done(function (response) {
            if (response.status == 'OK') {
                var data = response.data;
                showAlert('success', 'gen-alerts', 'New person was successfully added');
            }
            else if (response.status == 'error') {
                extractErrors(response.errors, function (error) {
                    writeAlert('error', 'form-alerts', error);
                });
                showAlert('error', 'form-alerts', '');
            }
        }).fail(function (jqXHR, textStatus) {
            showAlert('error', 'form-alerts', 'Please, check the connection.');
        });
    }

    var addForm = $('#add-person-form');
    $('#save-btn').click(function () {
        addForm.trigger("submit");
    });
    addForm.submit(addPerson);

    function updateField(id, field, newValue) {
        var params = {id: id, field: field, new_value: newValue};

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
        var column = editableGrid.getColumn(I);
        var editor = column.cellEditor();
    }
});