var hide=function(){
  box1.setAttribute("hidden", true);
  clear1.setAttribute("hidden", true);
  console.log("hide");
};

var show=function(){
  box1.removeAttribute("hidden")
  clear1.removeAttribute("hidden");
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
