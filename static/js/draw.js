var box= document.getElementById("box");
var boxy=box.getContext("2d");
var clear=document.getElementById("button");
var stop=document.getElementById("stop");
var intervalID;
boxy.fillStyle="black";

var x,y;
var prevX=0;
var prevY=0;

var updateMouse=function(e){
  //  prevX=x;
   // prevY=y;
    x = e.pageX-this.offsetLeft;
    y = e.pageY- this.offsetTop;
//    console.log(x);
   // console.log(y);
}


var animate=function(e){

  clearInterval(intervalID);

  var draw= function(){    
   boxy.fillRect(x,y,5,5);
   boxy.fill();
     
    };

    intervalID=window.setInterval(draw,.0000001);
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
stop.addEventListener("click", stopIt);
box.addEventListener("mousedown", animate);
box.addEventListener("mouseup", stopIt);
box.addEventListener("mousemove", updateMouse);
