var box= document.getElementById("box");
var boxy=box.getContext("2d");
var clear=document.getElementById("clear");
var stop=document.getElementById("stop");
var intervalID;
boxy.fillStyle="black";

var x,y;
var prevX=0;
var prevY=0;

var updateMouse=function(e){
    x = e.offsetX;
    y = e.offsetY;
}


var animate=function(e){

  clearInterval(intervalID);
  boxy.moveTo(x,y) //iniating so that it doesnt start from 0,0

  var draw= function(){
    boxy.lineWidth=5;
    boxy.lineTo(x,y);
    boxy.stroke();
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

clear.addEventListener("click", clearIt);
box.addEventListener("mousedown", animate);
box.addEventListener("mouseup", stopIt);
box.addEventListener("mousemove", updateMouse);
