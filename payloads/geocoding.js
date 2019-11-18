navigator.geolocation.getCurrentPosition(
    function (position) {
        var xhr = new XMLHttpRequest(); 
        xhr.open('GET', '/payload/' + position.coords.latitude + '_' + position.coords.longitude , true);
        xhr.send();
    }
);