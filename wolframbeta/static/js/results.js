var button=document.getElementById("button");
var code=document.getElementById("latexCode");

//shows source code & changes button label
var show=function(){
    code.removeAttribute("hidden");
    button.innerHTML="Hide Source Code";
};

//hides source code & changes button label
var hide=function(){
    code.setAttribute("hidden", true);
    button.innerHTML="Show Source Code";
};

//checks what status the page is in (if source code is shown or not)
//allows the page to alternate
var change=function(){
    if (button.innerHTML=="Show Source Code")
	show();
    else
	hide();
};


button.addEventListener("click", change);
