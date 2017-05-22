var hide=function(){
  var label= document.getElementById("label");
  label.setAttribute("hidden", true);
  var input= document.getElementByName("input2");
  input.setAttribute("hidden", true);
  console.log("hide");
};

var show=function(){
  var label= document.getElementById("label");
  label.removeAttribute("hidden");
  var input= document.getElementByName("input2");
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
