var box= document.getElementById("box");
var boxy=box.getContext("2d");
var clear=document.getElementById("button");
var stop=document.getElementById("stop");
var requestID;
boxy.fillStyle="black";


var animate=function(e){
  var x = e.offsetX;
  var y = e.offsetY;

  window.cancelAnimationFrame(requestID);

  var draw= function(e){
    	console.log(requestID);

    	boxy.fillRect(x,y,5,5);
    	boxy.fill();
      var x = e.offsetX;
      var y = e.offsetY;

	    requestID=window.requestAnimationFrame(draw(e));
    };

    draw(e);
};

var stopIt=function(){
    console.log(requestID);
    window.cancelAnimationFrame(requestID);
};

var clearIt= function(e){
  stopIt()
  e.preventDefault();
  boxy.clearRect(0,0,box.width, box.height);
  boxy.beginPath();
};

clear.addEventListener("click", clearIt);
stop.addEventListener("click", stopIt);
box.addEventListener("mousedown", animate);
box.addEventListener("mouseup", stopIt)
