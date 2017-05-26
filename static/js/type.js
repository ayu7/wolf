var label= document.getElementById("label");
var input= document.getElementById("input2");
var div= document.getElementById("col1");

//hides second input field & the text
var hide=function(){
  label.setAttribute("hidden", true);
  input.setAttribute("hidden", true);
  div.setAttribute("class", "col-lg-6 col-lg-offset-3");
  console.log("hide");
};

//shows second input field & the text
var show=function(){
  label.removeAttribute("hidden");
  input.removeAttribute("hidden");
  div.setAttribute("class", "col-lg-6");
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
