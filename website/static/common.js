const REGEXP_TICKET = /^[a-zA-Z]{3,8}-\d{3,8}$/
const REGEXP_FMID = /^[A-Z0-9$@]{6,8}$/
const REGEXP_APAR = /^(PH|UJ|PI|UI)\d{5}$/
const REGEXP_COMP = /^[)(a-zA-Z0-9\s]{3,18}(,[)(a-zA-Z0-9\s]{3,18}){0,4}$/

function validateInput(currentRestr, text) {
    var error = "";
    console.log("Validate called");
    console.log(currentRestr);
    if (currentRestr.isUrgent) {
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

function setVisibility(element, isShown){
    if(!isShown){
        $(element).attr("hidden", "");
    }
    else{
        $(element).removeAttr("hidden");
    }
}

function setError(errorForId, error, isVisible) {
    var errorLabel = $("div[errorFor='" + errorForId + "']")[0]
    errorLabel.innerText = error
    if(!isVisible)
        setVisibility(errorLabel, false)
    else
        setVisibility(errorLabel, true)
}

function setElementError(element, isError){
    if(isError){
        element.classList.add('is-invalid')
    }
    else{
        element.classList.remove('is-invalid')
    }

}

function setEnabled(element, isEnabled){
    if(isEnabled)
        element.removeAttribute('disabled')
    else
        element.setAttribute('disabled', '')
}

function setElementWarningFlag(element, needFlag){
    var alertHtml = '<svg class="flag" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" ' +
    'class="bi bi-emoji-frown" viewBox="0 0 16 16">' +
    '<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>' +
    '<path d="M4.285 12.433a.5.5 0 0 0 .683-.183A3.5 3.5 0 0 1 8 10.5c1.295 0 2.426.703 ' +
    '3.032 1.75a.5.5 0 0 0 .866-.5A4.5 4.5 0 0 0 8 9.5a4.5 4.5 0 0 0-3.898 2.25.5.5 0 0 0 .183.683M7 6.5C7 ' +
    '7.328 6.552 8 6 8s-1-.672-1-1.5S5.448 5 6 5s1 .672 1 1.5m4 0c0 .828-.448 1.5-1 1.5s-1-.672-1-1.5S9.448 5 ' +
    '10 5s1 .672 1 1.5"/></svg>'
    const currentFlag = $(element).find("svg")
    if(currentFlag){
       currentFlag.remove()
    }
    if(needFlag){
        element.append(alertHtml)
   }
}

function isContainsErrors(element){
  console.log('Type:', element, typeof element)
  var invalEls1 = $(element).find('.is-invalid')
  var invalEls = $(element).contents().find('.is-invalid')
  console.log('invals', invalEls)
  console.log('invals1', invalEls1)
  var hasErrors = false
  if(invalEls.length > 0){
    Array.from(invalEls).forEach((invalEl) => {
        const result = ($(invalEls).attr("hidden") == "hidden" || $(invalEls).parent().attr("hidden") == "hidden" )
        if(!result){
            hasErrors = true
            return;
        }
    });
  }
  return hasErrors
}

function setSaveButtonAvalHook(){
    document.onclick = function() {
        
    }
    document.onkeyup = function() {

    }
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

function showTab(tabId){
    const tabElement = $('#' + tabId)
    //const triggerEl = document.querySelector('#myTab button[data-bs-target="#nav-trans"]')
    console.log('triggerFirstTabEl', tabElement)
    bootstrap.Tab.getOrCreateInstance(tabElement).show() // Select first tab
}


console.log("Common funcs loaded");

