var input=document.getElementById("label2");

//hides second upload button
var hide=function(){
  input.setAttribute("style", "display:none");
  console.log("hide");
};

//shows second upload button
var show=function(){
  input.removeAttribute("style");
  console.log("show");
};

//changes page dynamically
var change=function(){
  var selectBox = document.getElementById("operation");
  var selectedValue = selectBox.options[selectBox.selectedIndex].getAttribute("class");
  if (selectedValue==1)
    hide();
  else
    show();
};

var file1=function(fileName){
  var label=document.getElementById("label1");
  label.innerText=fileName;

};

var file2=function(fileName){
  var label=document.getElementById("label2");
  label.innerText=fileName;

};
