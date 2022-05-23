if('geolocation' in navigator){
    navigator.geolocation.getCurrentPosition(position=>{
      var latitude=position.coords.latitude;
      var longitude=position.coords.longitude;
      console.log(latitude,longitude);
      var Myelement = document.getElementById("query").value;
      var a= latitude.toString();
      var b= longitude.toString();
      var v= a.concat("+",b);
      var d = Myelement
      var t= d.concat(",",v);
      document.getElementById("query").value = t;
      console.log(t)
      },error=>{
      alert("Please allow location");
    });
  }
  else{
    alert("Not Supported");
  }