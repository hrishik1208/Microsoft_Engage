<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="static/bootstrap/css/bootstrap.min.css" >
    <title>Attendance Management Portal</title>
    {% block script %}{% endblock  %}
<body {% block style %}{% endblock  %} >
<div>
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color:#4E5460;position: relative;">
        <div >
          <!-- <a class="navbar-brand" href="#">Navbar</a> -->
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div style="font-size: 20px;padding-left: 40px;" class="collapse navbar-collapse" id="navbarNav">
            <center>
            <ul class="navbar-nav" style="">
                <li class="nav-item">
                    <a style="font-size: 20px;padding-left: 40px;color: white;" class="nav-link active" aria-current="page" href="#"><div class="dropdown">
                      <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
                        Hi Instructor. {% block name %} {% endblock %}
                      </button>
                      <div class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                      <form method="POST" action="/logout">
                          {% csrf_token %}
                          <button class="form-control btn-primary btn" type="submit">Logout</button>
                      </form></div>
                    </div></a>
                  </li>
                  
              <li class="nav-item">
                <a style="font-size: 20px;color: white;margin-left:30px;" class="nav-link  {% block navlist1 %}  {% endblock  %}" aria-current="page" href="/">Home</a>
              </li>
              
              <li class="nav-item">
                <a style="font-size: 20px;margin-left: 60px;color: white;" class="nav-link {% block navlist2 %} {% endblock  %}" href="/course">Courses</a>
              </li>
              <li class="nav-item">
                <a style="font-size: 20px;margin-left: 60px;color: white;" class="nav-link {% block navlist3 %}  {% endblock  %}" href="/create">+ Create a Course</a>
              </li>
              <li class="nav-item">
                <a style="font-size: 20px;margin-left: 60px;color: white;" class="nav-link {% block navlist4 %}  {% endblock  %}" href="/insights">Records</a>
              </li>
              <li class="nav-item">
                <a style="font-size: 20px;margin-left: 60px;color: white;" class="nav-link {% block navlist5 %}  {% endblock  %}" href="/Request">Pending Requests</a>
              </li>
            </ul></center>
            
          </div>
        </div>
      </nav>
</div>


{% for message in messages %}
<div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
  <strong>Message : </strong> {{ message }}
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>{% endfor %}
<br>

{% block body %}

<hr>
<br><br>
<center>
    <div style="width: 60%;font-size: 20px">
        <div class="card card-body">
          <!-- Some placeholder content for the collapse component. This panel is hidden by default but revealed when the user activates the relevant trigger. -->
          <form  action='/course' method ="POST">
              {% csrf_token %}
                <div class="container"><h4>Course : {{course}}</h4></div>
                <hr>
            <div class="form-group">
              <label for="exampleInputPassword1">Active time duration</label><br> 
              <input type="number" class="form-control" name='time' id="exampleInputPassword1" placeholder="time in minutes" required >
            </div>
            <br>
            <hr>
           <div class="form-group">
            <div class="form-check">
              
              <input value="onboard" class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" onclick="fun1()" checked>
              <label class="form-check-label" for="flexRadioDefault">
                Disallow Geolocation
              </label>
            </div>
            <hr>
            <div class="form-check">
              <input value="onboard" class="form-check-input" type="radio" name="flexRadioDefault" onclick="fun2()" id="flexRadioDefault2" >
              <label class="form-check-label" for="flexRadioDefault">
                Allow Geolocation <br>
              </label>
            </div>
           </div>
           <div id="Fun1"></div><br>
           <div id="map"></div><br>
            
            
            <div >
              <input class="form-control" name="radius" id="Fun2" type="number" placeholder="Radius Distance in metres" required >
            </div>
            <br>
            <button value="{{course}}" name="course_name" type="submit" class="btn btn-primary">Start Taking Attendance</button>
          </form>
        </div>
      </div>
</center>
<br><br><br><br>
<script>
  var response=0;
  document.getElementById("Fun2").disabled = true;
  function fun1(){
    response=0;
    document.getElementById("Fun2").disabled = true;
    document.getElementById("Fun1").innerHTML = ' ';
    document.getElementById("map").innerHTML = ' ';
    document.getElementById("map").style.height = "0px";
  }


  function fun2(){
    document.getElementById("map").style.height = "400px";
    
    if('geolocation' in navigator){
      navigator.geolocation.getCurrentPosition(position=>{
        var latitude=position.coords.latitude;
        var longitude=position.coords.longitude;
        console.log(latitude,longitude);
      var a= latitude.toString();
      var b= longitude.toString();
      var v= a.concat("+",b);
        response=1;
        
       document.getElementById("flexRadioDefault2").value = v;
        document.getElementById("Fun2").disabled = false;
       
        var options = {
          center: {lat:latitude,lng:longitude},
          zoom:15
      }
  
      var map = new google.maps.Map(document.getElementById('map'),options);
  
      var markerOptions={
          position: new google.maps.LatLng(latitude,longitude),
          map: map
      }
  
      var marker= new google.maps.Marker(markerOptions)
    

        },error=>{
        alert("Please allow location and check your internet connectivity");
      });
    }
    else{
      alert("Not Supported");
    }
  }
  
  function initMap(){
    }
</script>
<script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCjIW074C0g8UlUxBGsYlxzhE1T2kKyFaU"></script>


{% endblock  %}

<script src="static/bootstrap/js/popper.min.js" ></script>
<script src="static/bootstrap/js/bootstrap.min.js" ></script>    
</body>
</html>