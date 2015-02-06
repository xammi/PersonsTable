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
    },
    selection: function (value) {
        return true;
    }
};

function apply(field, value) {
    return Validators[field](value);
}

function validate(params) {
    for (var field in Validators)
        if (Validators.hasOwnProperty(field))
            if (! apply(field, params[field])) {
                showAlert('error', 'form-alerts', 'Invalid field: ' + field);
                return false;
            }

    return true;
}

function writeAlert(kind, blockId, text) {
    var item;
    var block = $('#' + blockId);
    if (kind === 'success')
        item = block.children('.alert-success');
    else if (kind === 'error')
        item = block.children('.alert-danger');

    item.html(item.html() + '&nbsp; \n  &nbsp;' + text);
    return item;
}

function showAlert(kind, blockId, text) {
    var item = writeAlert(kind, blockId, text);

    if (item.css('display') == 'none') {
        item.fadeIn('slow').delay(10000).fadeOut('slow', function () {
            item.html('');
        });
    }
}

function extractErrors(errors, action) {
    for (var error in errors)
        if (errors.hasOwnProperty(error))
            action(errors[error]);
}

function extractFieldErrors(errors, action) {
    for (var field in errors)
        if (errors.hasOwnProperty(field))
            extractErrors(errors[field], action);
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
        {
            name: "selection",
            label: "#",
            datatype: "boolean",
            editable: true
        }
    ];
}

$(document).ready(function () {
    var editableGrid = new EditableGrid("Address Book");
    var metadata = prepareMeta();

    function updateTable() {
        $('#spinner-modal').modal('show');
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
                $('#spinner-modal').modal('hide');
            }
        }).fail(function (jqXHR, textStatus) {
            showAlert('error', 'gen-alerts', 'Unable to update. Please, check the connection.');
            $('#spinner-modal').modal('hide');
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
                showAlert('success', 'form-alerts', 'New person was successfully added');
                editableGrid.append(data.id, data.values);
            }
            else if (response.status == 'error') {
                extractFieldErrors(response.errors, function (error) {
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
            if (response.status == 'OK') {}
            else if (response.status == 'error') {
                extractErrors(response.errors, function (error) {
                    writeAlert('error', 'gen-alerts', error);
                });
                showAlert('error', 'gen-alerts', '');
            }
        }).fail(function (jqXHR, textStatus) {
            showAlert('error', 'form-alerts', 'Please, check the connection.');
        });
    }

    editableGrid.modelChanged = function(rowIndex, columnIndex, oldValue, newValue) {
        var id = editableGrid.getRowId(rowIndex);
        var field = editableGrid.getColumnName(columnIndex);

        if (field === 'selection') {
            selectionChanged(rowIndex, id, oldValue, newValue);
            return;
        }

        if (apply(field, newValue)) {
            updateField(id, field, newValue);
        }
        else {
            showAlert('error', 'gen-alerts', 'Invalid update: ' + field);
            editableGrid.setValueAt(rowIndex, columnIndex, oldValue);
        }
    };

    var selectedIds = [];
    var deleter = $('#deleter');

    function selectionChanged(rowIndex, id, oldValue, newValue) {
        var row = editableGrid.getRow(rowIndex);

        if (oldValue === true && newValue === false) {
            $(row).removeClass('selected');

            selectedIds = $.grep(selectedIds, function(value) {
                return value !== id;
            });
            if (selectedIds.length === 0)
                deleter.addClass('disabled');
        }

        if (oldValue === false && newValue === true) {
            $(row).addClass('selected');
            selectedIds.push(id);
            deleter.removeClass('disabled');
        }
    }

    function deleteSelected() {
        var params = {ids: selectedIds + ''};

        $.ajax({
            url: '/delete/',
            type: 'POST',
            data: params,
            dataType: 'json'
        }).done(function (response) {
            if (response.status == 'OK' ) {
                showAlert('success', 'gen-alerts', 'Successfully deleted');

                var ids = response.data.ids.split(',');
                for (var I = 0; I < ids.length; I++)
                    editableGrid.removeRow(ids[I]);

                selectedIds = [];
                deleter.addClass('disabled');
            }
            else if (response.status == 'error') {
                extractErrors(response.errors, function (error) {
                    writeAlert('error', 'gen-alerts', error);
                });
                showAlert('error', 'gen-alerts', '');
            }
        }).fail(function (jqXHR, textStatus) {
            showAlert('error', 'gen-alerts', 'Please, check the connection.');
        });
    }

    deleter.click(deleteSelected);
    editableGrid.filter('');
});