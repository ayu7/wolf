
//set 1
var box= document.getElementById("box");
var boxy=box.getContext("2d");
var boxContent=document.getElementById("boxContent");
var clear=document.getElementById("clear");
var div=document.getElementById("canvas");

//set2
var box1= document.getElementById("box1");
var boxy1=box1.getContext("2d");
var box1Content=document.getElementById("box1Content");
var clear1=document.getElementById("clear1");

var intervalID;
var x,y;

var fillBack=function(x){ // 0 fills both canvas, 1 fills first, 2 fills second
    if (x==0 || x==1){
	boxy.fillStyle="white";
	boxy.fillRect(0,0,box.width, box.height);
}
    if (x==0 || x==2){
	boxy1.fillStyle="white";
	boxy1.fillRect(0,0,box.width, box.height);
}
    console.log("fill"+x);
};

fillBack(0);

//updates mouse position everytime it moves
var updateMouse=function(e){
    x = e.offsetX;
    y = e.offsetY;
};

var animate=function(){

  clearInterval(intervalID);
  var c= this.getContext("2d"); //getting context again here allows this function to be used for both canvas
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
   var con1 = box.toDataURL('image/jpg', 1.0);
   var con2 = box1.toDataURL('image/jpg', 1.0);
   console.log("entered");
   console.log(con1);
   boxContent.setAttribute("value", con1); //updates dataURL info everytime mouse up
   box1Content.setAttribute("value", con2);
   boxContent.setAttribute("value", box.toDataURL());
   box1Content.setAttribute("value", box1.toDataURL());
};

//need two clear functions instead of using this because the buttons aren't tied to the canvas
var clearIt= function(e){
  stopIt;
  e.preventDefault();
  boxy.clearRect(0,0,box.width, box.height);
  boxy.beginPath();
  fillBack(1);
};

var clearIt1= function(e){
  stopIt;
  e.preventDefault();
  boxy1.clearRect(0,0,box.width, box.height);
  boxy1.beginPath();
  fillBack(2);
};

clear.addEventListener("click", clearIt);
box.addEventListener("mousedown", animate);
box.addEventListener("mouseup", stopIt);
box.addEventListener("mousemove", updateMouse);

clear1.addEventListener("click", clearIt1);
box1.addEventListener("mousedown", animate);
box1.addEventListener("mouseup", stopIt);
box1.addEventListener("mousemove", updateMouse);

//hides second canvas
var hide=function(){
  box1.setAttribute("hidden", true);
  clear1.setAttribute("hidden", true);
  clear1.removeAttribute("class");
  div.setAttribute("class", "col-lg-6 col-lg-offset-3");
  console.log("hide");
};

//shows second canvas
var show=function(){
  box1.removeAttribute("hidden");
  clear1.removeAttribute("hidden");
  clear1.setAttribute("class", "btn btn-primary btn-sm"); //class is removed/added because once it is added the hidden attribute doesn't work anymore for some reason??
  div.setAttribute("class", "col-lg-6");
  console.log("show");
};

//dynamically changes the page as user selects options
var change=function(){
  var selectBox = document.getElementById("operation");
  var selectedValue = selectBox.options[selectBox.selectedIndex].getAttribute("class");
  if (selectedValue==1)
    hide();
  else
    show();
};


/*
var dataURL = canvas.toDataURL();
$(function() {
    $(form).submit(function(e) {
          e.preventDefault();
          $.ajax({
              type: "POST",
              url: "script.php",
              data: { 
                 imgBase64: dataURL
              }
         }).done(function(o) {
              console.log('saved image'); 
              $.post(url, form.serialize(), function(data) {
                     console.log('saved form')
              };
    });*/
