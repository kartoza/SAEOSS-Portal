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

    $.ajax({
        type: 'POST',
        url: _url,
        contentType: 'application/json',
        data: JSON.stringify({ 'value': data }),
        success: function(resultData) { 
            const obj = JSON.parse(resultData)
            // for(var i = 0; i < obj["message"].length; i++){
            //     obj["message"][i]["message"] = JSON.stringify(obj["message"][i]["message"])
            // }
            console.log(obj)
            try {
                $.each(obj, function (key, validTypeObj) {
                    $.each(validTypeObj, function (idx, resourceId) {
                        let rowData = table.row(`#${resourceId}`).data();
                        if(key == "invalid"){
                            var error_message = ""
                            for(var i = 0; i < obj["message"].length; i++){
                                console.log(obj["message"][i]["resource_id"])
                                if(obj["message"][i]["resource_id"] == resourceId){
                                    // error_message = JSON.stringify(obj["message"][i]["message"])
                                    error_message = obj["message"][i]["message"]
                                }
                            }
                            
                            rowData.validity = `<button type="button" data-toggle="modal" class="btn btn-primary" data-target="#modal-${resourceId}">${key}</button>`
                            
                            document.getElementById("feedback").innerHTML += `<!-- Modal -->
                            <div class="modal fade" id="modal-${resourceId}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog" role="document">
                                <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="exampleModalLabel">Error Message</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>
                                <div class="modal-body">
                                    ${error_message}
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                </div>
                                </div>
                            </div>
                            </div>`;
                        }
                        else{
                            rowData.validity = key;
                        }
                        table.row(`#${resourceId}`).data(rowData);
                    });
                });
            } catch (error) {
                console.log(error)
            }

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