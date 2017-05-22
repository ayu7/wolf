var box= document.getElementById("box");
var boxy=box.getContext("2d");
var clear=document.getElementById("clear");
var box1= document.getElementById("box1");
var boxy1=box1.getContext("2d");
var clear1=document.getElementById("clear1");
var intervalID;
var one=document.getElementsByClassName("1");
var two=document.getElementsByClassName("2");
var x,y;

var updateMouse=function(e){
    x = e.offsetX;
    y = e.offsetY;
}

var animate=function(){

  clearInterval(intervalID);
  var c= this.getContext("2d");
  c.moveTo(x,y) //iniating so that it doesnt start from 0,0

  var draw= function(){
    c.lineWidth=5;
    c.lineTo(x,y);
    c.stroke();
};
    intervalID=window.setInterval(draw,1);
};

var stopIt=function(){
   clearInterval(intervalID);
};

var clearIt= function(e){
  stopIt;
  e.preventDefault();
  boxy.clearRect(0,0,box.width, box.height);
  boxy.beginPath();
};

var clearIt1= function(e){
  stopIt;
  e.preventDefault();
  boxy1.clearRect(0,0,box.width, box.height);
  boxy1.beginPath();
};

clear.addEventListener("click", clearIt);
box.addEventListener("mousedown", animate);
box.addEventListener("mouseup", stopIt);
box.addEventListener("mousemove", updateMouse);
clear1.addEventListener("click", clearIt1);
box1.addEventListener("mousedown", animate);
box1.addEventListener("mouseup", stopIt);
box1.addEventListener("mousemove", updateMouse);

var hide=function(){
  box1.setAttribute("hidden", true);
  clear1.setAttribute("hidden", true);
  console.log("hide");
};

var show=function(){
  box1.removeAttribute("hidden")
  clear1.removeAttribute("hidden");
  console.log("show");
};

for (i=0; i<one.length;i++){
  one[i].addEventListener("click", hide);
};

for (i=0; i<two.length;i++){
  two[i].addEventListener("click", show);
};
