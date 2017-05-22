var hide=function(){
  var input=document.getElementById("input2");
  input.setAttribute("hidden", true);
  console.log("hide");
};

var show=function(){
  var input=document.getElementById("input2");
  input.removeAttribute("hidden");
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
