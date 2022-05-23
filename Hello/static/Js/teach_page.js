var i = document.getElementById('val').innerHTML; 
console.log(i); 
document.getElementById("val").innerHTML = ""; 
var x=setInterval(function(){ 
var now =new Date().getTime();
var diff=i-now;
diff = diff / 1000 ;
var num=Math.floor(diff/60);
var str=num.toString();
if (num<0){
    str="0";
}

var num1 = Math.floor(diff % 60);
var str1=num1.toString();
if(num1 <0 ){
    str1="0";
}
var fin=str.concat(" : ",str1);
document.getElementById("val").innerHTML = fin;
console.log(fin);
if (num <=0 && num1<=0){
    location.href = "/teacher_page";
}
}, 1000 )