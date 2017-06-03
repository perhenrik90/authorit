/***********************************************
 * Navbar creates the upper navigationbar 
 * 
 * @author Per-Henrik Kvalnes
 ***********************************************/

// setup for all divtags with classname 'slide' 
function initNavBar(se)
{
    
    // data objects / models / got from slideengine.js (!)

    se.slides = document.getElementsByClassName("slide");
    nav = document.getElementById("menu");
    fluid = document.createElement("div");
    fluid.className = "container-fluid";
    nav.appendChild(fluid);

    // append a header
    head = makeNavHeader();
    fluid.appendChild(head);

    menu = document.createElement("ul");
    fluid.appendChild(menu);
    menu.className = "nav navbar-nav";

    /** loop through the stuff and setup menu **/
    for(i = 0; i < se.slides.length; i ++)
    {
	obj = se.slides[i];
	if(obj.title)
	{
	    li = document.createElement("li");
	    a = document.createElement("a");
	    a.id = i;
	    li.appendChild(a);

	    a.innerHTML = obj.title;
	    a.onclick = se.setSlideByTitle;
	    menu.appendChild(li);
	}
    }
}




function makeNavHeader()
{
    head = document.createElement("div");
    head.className = "navbar-header";


    brand = document.createElement("div");
    brand.className =  "navbar-brand";
    //brand.innerHTML = CONF["projectname"];
    head.appendChild(brand);
    
    return head;
    
}
