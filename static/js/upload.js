var hide=function(){
  var input=document.getElementById("input2");
  input.setAttribute("style", "display:none");
  console.log("hide");
};

var show=function(){
  var input=document.getElementById("input2");
  input.removeAttribute("style");
  console.log("show");
};

var change=function(){
  var selectBox = document.getElementById("operation");
  var selectedValue = selectBox.options[selectBox.selectedIndex].getAttribute("class");
  if (selectedValue==1)
    hide();
  else
    show();
};
