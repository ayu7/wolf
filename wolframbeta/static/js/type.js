var col1= document.getElementById("col1");
var col2= document.getElementById("col2");

//hides second input field & the text
var hide=function(){
  col2.setAttribute("style", "display:none");
  col1.setAttribute("class", "col-lg-6 col-lg-offset-3");
  console.log("hide");
};

//shows second input field & the text
var show=function(){
  col2.removeAttribute("style");
  col1.setAttribute("class", "col-lg-6");
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
