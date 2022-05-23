document.getElementById("Fun2").disabled = true;
function fun1(){

  document.getElementById("Fun2").disabled = true;
  document.getElementById("Fun1").innerHTML = ' ';
}


function fun2(){
  if('geolocation' in navigator){
    navigator.geolocation.getCurrentPosition(position=>{
      var latitude=position.coords.latitude;
      var longitude=position.coords.longitude;
      console.log(latitude,longitude);
    var a= latitude.toString();
    var b= longitude.toString();
    var v= a.concat("+",b);

      
     document.getElementById("flexRadioDefault2").value = v;
      document.getElementById("Fun2").disabled = false;
      document.getElementById("Fun1").innerHTML = '<hr><p>Info About this project</p> <img width="100%" src="/static/images/globe.jpg">';

      },error=>{
      alert("Please allow location");
    });
  }
  else{
    alert("Not Supported");
  }
}