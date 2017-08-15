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
    menu = document.getElementById("menu");

    // append a header
    // head = makeNavHeader();
    // fluid.appendChild(head);

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
