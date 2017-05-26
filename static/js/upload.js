var input=document.getElementById("input2");

//hides second upload button
var hide=function(){
  input.setAttribute("style", "display:none");
  console.log("hide");
};

//shows second upload button
var show=function(){}
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
