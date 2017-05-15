var box= document.getElementById("box");
var boxy=box.getContext("2d");
var clear=document.getElementById("button");
var stop=document.getElementById("stop");
var requestID;
boxy.fillStyle="black";

var x,y;
var prevX,prevY=0;

var updateMouse=function(e){
    prevX=x;
    prevY=y;
    x = e.pageX-this.offsetLeft;
    y = e.pageY- this.offsetTop;
}


var animate=function(e){

  window.cancelAnimationFrame(requestID);

  var draw= function(){
    console.log(requestID);
    
    while(x!=prevX){
	prevX++;
	 boxy.fillRect(prevX,y,5,5);
    boxy.fill();
    }
    
    boxy.fillRect(x,y,5,5);
    boxy.fill();
   
     
    requestID=window.requestAnimationFrame(draw);
    };

    draw();
};

var stopIt=function(){
    console.log(requestID);
    window.cancelAnimationFrame(requestID);
};

var clearIt= function(e){
  stopIt();
  e.preventDefault();
  boxy.clearRect(0,0,box.width, box.height);
  boxy.beginPath();
};

clear.addEventListener("click", clearIt);
stop.addEventListener("click", stopIt);
box.addEventListener("mousedown", animate);
box.addEventListener("mouseup", stopIt);
box.addEventListener("mousemove", updateMouse);
