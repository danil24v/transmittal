const REGEXP_TICKET = /^[a-zA-Z]{3,8}-\d{3,8}$/
const REGEXP_FMID = /^[A-Z0-9$@]{6,8}$/
const REGEXP_APAR = /^(PH|UJ|PI|UI)\d{5}$/
const REGEXP_COMP = /^[)(a-zA-Z0-9\s]{3,18}(,[)(a-zA-Z0-9\s]{3,18}){0,4}$/

function validateInput(restrDict, key, text) {
    var error = "";
    console.log("Validate called");
    var currentRestr = restrDict[key];
    console.log(currentRestr);
    if (currentRestr.isUrgent.toLowerCase() == "true") {
        if (text.trim().length < 1) {
            error = 'Field is empty!';
            return error;
        }
    }
    if (text.length > currentRestr.maxsize) {
        error = 'Maximum size of ' + currentRestr.maxsize + ' symbols exceed by ' + (currentRestr.maxsize - text.length) + ' symbols.';
        return error;
    }
    var lines = text.split("\n");
    var i = 0;
    for (var _i = 0, lines_1 = lines; _i < lines_1.length; _i++) {
        var line = lines_1[_i];
        (function (line) {
            if (line.length > currentRestr.linelen) {
                error = "Maximum line length exceed on line " + i + " , max len: " + currentRestr.linelen.toString();
                return error;
            }
            if (currentRestr.regexp != "") {
                var re = new RegExp(currentRestr.regexp);
                if (!re.test(line)) {
                    error = "Line " + i + " do not match " + currentRestr.regexp + " regexp. Please check it for special symbols.";
                }
            }
        })(line);
        i++;
    }
    return error;
}

function setError(errorForId, error, isVisible) {
    var errorLabel = $("div[errorFor='" + errorForId + "']")[0]
    errorLabel.innerText = error
    if(!isVisible)
        errorLabel.style.display = "none"
    else
        errorLabel.style.display = ""
}

function setElementError(element, isError){
    var btnSave = $("[name='btnSave']")[0]
    if(isError){
        element.classList.add('is-invalid')
        setEnabled(btnSave, false)
    }
    else{
        element.classList.remove('is-invalid')
        setEnabled(btnSave, true)
    }
}

function setEnabled(element, isEnabled){
    if(isEnabled)
        element.removeAttribute('disabled')
    else
        element.setAttribute('disabled', '')
}

function doReq(method, url, data_dict, good_callback, bad_callback){
    $.ajax({
        url: url,
        type: method,
        data: data_dict,
        success: function(data) {
            console.log("GOOD DATA")
            if(good_callback != null)
                good_callback(data)
            else
                location.reload()
            return;
        },
        error: function(data) {
            console.log("BAD DATA DATA")
            if(bad_callback != null)
                bad_callback(data)
            else
                alert(data.responseText)
            return;
        }
    });
}


console.log("Common funcs loaded");

