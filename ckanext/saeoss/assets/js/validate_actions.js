function toTitleCase(str) {
  return str.toLowerCase().split(' ').map(function (word) {
    return (word.charAt(0).toUpperCase() + word.slice(1));
  }).join(' ');
}

$(document).ready(function () {
    $('#feedback').html('')

    document.getElementById("select_data").style.display = "block"
    $.ajax({
        type: 'GET',
        url: "/validator/retrieve_metadata/",
        success: function(resultData) {
            let resourceArr = JSON.parse(resultData)
            resourceArr = resourceArr.map((resource) => {
                resource.validity = resource.validity ? resource.validity : '';
                return resource
            });
            let resource = `<p>Click on the table row to select resources</p>`;
            let colNames = [
                'resource_name',
                'resource_id',
                'url',
                'url_type',
                'format',
                'package_name',
                'validity'
            ];
            let columns = [];
            if (resourceArr.length > 0) {
                for (let i = 0; i < colNames.length; i++)
                    columns.push({
                        title: toTitleCase((colNames[i].split('_')).join(' ')),
                        data: colNames[i].replace(/\./g, '\\.')
                    });
            }
            resource += '<table id="resource-table"></table>';
            document.getElementById("select_data").innerHTML = resource;
            const table = new DataTable('#resource-table', {
                data: resourceArr,
                columns: columns,
                rowId: 'resource_id',
                search: {
                    regex: true
                }
            });

            table.on('click', 'tbody tr', function (e) {
                e.currentTarget.classList.toggle('selected');
            });

            $('#btn-validate-all').click(function () {
                validate(table, 'validate_all')
            });
            $('#btn-validate-selected').click(function () {
                validate(table, 'validate_selected')
            });

        },
        error: function(resultData){
            alert("Something went wrong!")
        }
    });
})

function validate(table, validationType){
    const buttonId = validationType == 'validate_all' ? 'btn-validate-all': 'btn-validate-selected';
    const buttonText = validationType == 'validate_all' ? 'Validate All': 'Validate Selected';
    $(`#${buttonId}`)[0].innerHTML = "Submitting...";
    $('btnSubmit').attr('disabled', true);
    let _url = ""
    data = []
    
    if(validationType == "validate_all"){
        _url = "/validator/validate_all/"
    }
    else{
        _url = "/validator/validate_selection/"
        for (let i = 0; i < table.rows('.selected').data().length; i++) {
            data.push(table.rows('.selected').data()[i].resource_id);
        }
    }

    console.log(data)

    $.ajax({
        type: 'POST',
        url: _url,
        contentType: 'application/json',
        data: JSON.stringify({ 'value': data }),
        success: function(resultData) { 
            const obj = JSON.parse(resultData)
            $.each(obj, function (key, validTypeObj) {
                $.each(validTypeObj, function (idx, resourceId) {
                    let rowData = table.row(`#${resourceId}`).data();
                    rowData.validity = key;
                    table.row(`#${resourceId}`).data(rowData);
                });
            });
            $(`#${buttonId}`)[0].innerHTML = buttonText;
            $('btnSubmit').attr('disabled', true);
        },
        error: function(resultData){
            $(`#${buttonId}`)[0].innerHTML = buttonText;
            $('btnSubmit').attr('disabled', true);
            alert("Something went wrong!")
        }
    });
}