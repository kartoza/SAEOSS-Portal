function handleChange(radio){
    var typeOf = radio.value
    $('#feedback').html('')

    if(typeOf == 'validate_all'){
        document.getElementById("select_data").style.display = "none"
    }
    else{
        document.getElementById("select_data").style.display = "block"
        $.ajax({
            type: 'GET',
            url: "/validator/retrieve_metadata/",
            success: function(resultData) { 
                
                const obj = JSON.parse(resultData)
                var resource = `<p>Select multiple resources to validate:</p>`;
                for (var i = 0; i < obj.length; i++){
                    resource += `
                        <div id=${obj[i]["package_id"]}>
                        <h4>Dataset: ${obj[i]["package_name"]}</h4>
                    `
                    for(var x = 0; x < obj[i]["resources"].length; x++){
                        var resource_name= obj[i]["resources"][x]["resource_name"]
                        if(resource_name == ""){
                            resource_name = "undefined"
                        }
                        resource += `
                            <input type="checkbox" name='resource_validate' class='resource_validate' value='${obj[i]["resources"][x]["resource_id"]}'/>
                            <label>Name: ${resource_name} (url: ${obj[i]["resources"][x]["url"]})</label>
                            <br>
                        `
                    }

                    resource += `
                        </div>
                    `
                }
                document.getElementById("select_data").innerHTML = resource
            },
            error: function(resultData){
                alert("Something went wrong!")
            }
        });
    }
}

function successMessage(obj){
    var success_msg = ``;
    if(obj[0]["success"].length > 0){
    
        success = `<h4 style="color:green">The following resources have passed validation:</h4>`
        for(var i = 0; i < obj[0]["success"].length; i++){
            success_msg += `
            <p>Resource id: ${obj[0]["success"][i]["resource_id"]}</p>
            <p>Resource name: ${obj[0]["success"][i]["resource_name"]}</p>
            <p>Resource url name: ${obj[0]["success"][i]["file_url"]}</p> 
            <p>Dataset saved to: ${obj[0]["success"][i]["package_name"]}</p> 
            <hr>
            `
        }
    }
    return success_msg
}

function errorMessage(obj){
    var error_msg = ``;
    if(obj[0]["error"].length > 0){
        console.log(obj[0]["error"][0]["resource_name"])
        error_msg = `<h4 style="color:red">The following resources have not passed validation:</h4>`
        for(var i = 0; i < obj[0]["error"].length; i++){
            error_msg += `
            <p>Resource id: ${obj[0]["error"][i]["resource_id"]}</p>
            <p>Resource name: ${obj[0]["error"][i]["resource_name"]}</p>
            <p>Resource url name: ${obj[0]["error"][i]["file_url"]}</p> 
            <p>Dataset saved to: ${obj[0]["error"][i]["package_name"]}</p> 
            <p>Error message: ${obj[0]["error"][i]["message"]} </p>
            <hr>
            `
        }
    }
    return error_msg
}

function validate(){

    var typeOf = document.querySelector('input[name="validation"]:checked').value
    document.getElementById("btnSubmit").innerHTML = "Submitting...";
    document.getElementById("btnSubmit").disabled = true;
    var _url = ""
    data = []
    
    if(typeOf == "validate_all"){
        _url = "/validator/validate_all/"
    }
    else{
        _url = "/validator/validate_selection/"
        var checkedVals = $('.resource_validate:checkbox:checked').map(function(){
            return this.value;
        }).get()

        data = checkedVals
    }

    console.log(data)

    $.ajax({
        type: 'POST',
        url: _url,
        contentType: 'application/json',
        data: JSON.stringify({ 'value': data }),
        success: function(resultData) { 
            const obj = JSON.parse(resultData)
            // obj = resultData
            document.getElementById("btnSubmit").innerHTML = "Submit";
            document.getElementById("btnSubmit").disabled = false;
            
            var html = `<h4>Results:</h4> ${successMessage(obj)} ${errorMessage(obj)}`;
            document.getElementById("feedback").innerHTML = html
        },
        error: function(resultData){
            document.getElementById("btnSubmit").innerHTML = "Submit";
            document.getElementById("btnSubmit").disabled = false;
            alert("Something went wrong!")
        }
    });
}