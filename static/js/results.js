var button=document.getElementById("button");
var code=document.getElementById("latexCode");

var show=function(){
    code.removeAttribute("hidden");
    button.innerHTML="Hide Source Code";
};

var hide=function(){
    code.setAttribute("hidden", true);
    button.innerHTML="Show Source Code";
};

var change=function(){
    if (button.innerHTML=="Show Source Code")
	show();
    else
	hide();
};


button.addEventListener("click", change);
