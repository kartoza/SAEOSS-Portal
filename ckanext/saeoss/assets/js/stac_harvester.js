function toTitleCase(str) {
    return str.toLowerCase().split(' ').map(function (word) {
      return (word.charAt(0).toUpperCase() + word.slice(1));
    }).join(' ');
  }

function create_stac(){
    data = [
        {
            "url": document.getElementById("_url").value,
            "number_records": document.getElementById("number_records").value,
            "owner_org": document.getElementById("field-organizations").value
        }
    ]

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/stac_harvest/create/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        'value': data
    }));

    alert("Harvesting Job has been created! ")
}

function view_stac_jobs(){
    $('#feedback').html('')

    document.getElementById("stac_jobs").style.display = "block"
    $.ajax({
        type: 'GET',
        url: "/stac_harvest/view_jobs/",
        success: function(resultData) {
            let resourceArr = JSON.parse(resultData)
            console.log(resourceArr)
            resourceArr = resourceArr.map((resource) => {
                resource.validity = resource.validity ? resource.validity : '';
                return resource
            });
            let resource = `<p>Click on the table row to select resources</p>`;
            let colNames = [
                'harvester_id',
                'user',
                'owner_org',
                'url',
                'number_records',
                'status',
                'message'
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
            document.getElementById("stac_jobs").innerHTML = resource;
            const table = new DataTable('#resource-table', {
                data: resourceArr,
                columns: columns,
                rowId: 'resource_id',
                search: {
                    regex: true
                }
            });

        },
        error: function(resultData){
            alert("Something went wrong!")
        }
    });
}