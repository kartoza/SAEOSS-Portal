function maxLengthCheck(object) {
    if (object.value.length > object.maxLength) {
        object.value = object.value.slice(0, object.maxLength)
    }
}

function getUrlParameter(param) {
    let sPageURL = window.location.search.substring(1),
        URLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < URLVariables.length; i++) {
        sParameterName = URLVariables[i].split('=');
        if (sParameterName[0] === param) {
            return sParameterName[1];
        }
    }
    return false;
}

function removeParameter(key, url) {
    let returnURL = url.split("?")[0],
        parameter,
        parameters_arr = [],
        queryString = (url.indexOf("?") !== -1) ? url.split("?")[1] : "";
    if (queryString !== "") {
        parameters_arr = queryString.split("&");
        for (let i = parameters_arr.length - 1; i >= 0; i -= 1) {
            parameter = parameters_arr[i].split("=")[0];
            if (parameter === key) {
                parameters_arr.splice(i, 1);
            }
        }
        if (parameters_arr.length) returnURL = returnURL + "?" + parameters_arr.join("&");
    }
    return returnURL;

}

function titleCase(str) {
  return str.toLowerCase().split(' ').map(function(word) {
    return (word.charAt(0).toUpperCase() + word.slice(1));
  }).join(' ');
}

$(document).ready(function() {
    let userAgent = navigator.userAgent;
    let browserName;

    if (userAgent.match(/chrome|chromium|crios/i)) {
        browserName = "chrome";
    } else if (userAgent.match(/firefox|fxios/i)) {
        browserName = "firefox";
    } else if (userAgent.match(/safari/i)) {
        browserName = "safari";
    } else if (userAgent.match(/opr\//i)) {
        browserName = "opera";
    } else if (userAgent.match(/edg/i)) {
        browserName = "edge";
    } else {
        browserName = "No browser detection";
    }
    if (!['chrome', 'safari', 'opera', 'edge'].includes(browserName)) {
        if (localStorage.getItem("hideBrowserCompatibilityWarning")) {
            return
        }
        $('.modal-title').text(`${titleCase(browserName)} browser detected!`);
        $('.modal-body').text(
          'Some features might not be working properly. Please use Chrome or Safari!'
        );
        $('#browserAlert .close').click(() => {
            let hideWarning = $('#hideBrowserCompatibilityWarning').is(':checked');
            if (hideWarning) {
                localStorage.setItem("hideBrowserCompatibilityWarning", true)
            }
            $('#browserAlert').hide();
        })
        $('#browserAlert').show();
    }
});