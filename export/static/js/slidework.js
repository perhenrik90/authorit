/************************************************
 * Slidework defines the framework for slides
 * Can be seen as the 'slide engine'.
 * 
 * @author Per-Henrik Kvalnes
 ***********************************************/

// setup for all divtags with classname 'slide' 
function initSlideEngine()
{
    var se = new Object(); // define a slide engine

    // data objects / models
    se.slides = document.getElementsByClassName("slide");
    se.index = 0;

    // check if TinCan is used
    if(window.location.search.indexOf("tincan=true")>0)
    {
	console.log("Tincan / xAPI is turned on.");
    }
    
    // updates the view 
    se.updateView = function()
    {
	for(var i = 0; i < se.slides.length; i ++)
	{
	    slide = se.slides[i];
	    slide.style.display = "none";
	    if(i == se.index)
	    {
		slide.style.display = "";
	    }
	}

	$("#course_progress_bar").css('width', (se.index/(se.slides.length-1)*100)+"%")
	
    }

    // jump to next slide
    se.nextSlide = function()
    {
	// only if there is a next slide
	if(se.index < se.slides.length-1)
	{
	    se.index += 1;
	}
	if(se.index == se.slides.length-1)
	{
		setCourseComplete();
	}

	se.updateView();
    }

    se.setSlideByTitle = function(e)
    {
	title = e.target.innerHTML;
	for(i = 0; i < se.slides.length; i++)
	{
	    obj = se.slides[i];
	    if(obj.title == title)
	    {
		se.index = i;
	    }
	}
	se.updateView();
    }

    // go back to previous slide
    se.previousSlide = function()
    {
	if(se.index>0)
	{
	    se.index -= 1;
	}
	else{se.index = 0;}
	se.updateView();
    }


    // set next button inactive
    se.disableNextButton = function()
    {
	nextbtn.className = "btn-disabled";
	nextbtn.onclick = "";
    }
    
    // set next button active
    se.enableNextButton = function()
    {
	nextbtn.className = "btn";
	nextbtn.onclick = se.nextSlide;
    }



    // create navbar buttons
    navbar = document.getElementById("navBar");
    
    // if statusbar, create it
    bardiv = document.getElementById("bardiv");
    bardiv.className = "progress";
    pbar = document.createElement("div");
    bardiv.appendChild(pbar);
    
    pbar.className = "progress-bar";
    pbar.role = "progressbar";
    pbar.id = "course_progress_bar";


    // init reporting tools 
    // if(CONF['type'] == "scorm1.2")
    // {
    // 	SCORMInit();
    // }
    // if(CONF['type'] == "tincan")
    // {
    // 	TinCanInit();
    // }

    // setup keybindings fo the document
    document.onkeydown = function(e)
    {
	switch(e.which)
	{
	    // case of left key
	    case 37: se.previousSlide();
	    break;
	    // case of right key
	    case 39: se.nextSlide();
	    break;
	}
    }


    
    // update the view before starting 
    se.updateView()
    return se;
}


function setCourseComplete()
{
    // if(CONF['type'] == "scorm1.2")
    // {
    // 	SCORMComplete()
    // }	
    // if(CONF['type'] == "tincan")
    // {
    // 	TinCanComplete()
    // }
}




// SCORM tools
// Uses the Scorm Libary
function SCORMInit()
{
	s = pipwerks.SCORM.init()	
	if(!s){alert("Could not connect to the LMS!")}
}

function SCORMComplete()
{
	s = pipwerks.SCORM.set('cmi.core.lesson_status', 'completed')
	if(!s){alert('Could not set the course to completed!');}
	SCORMQuit();
}

function SCORMQuit()
{
	pipwerks.SCORM.quit()
}

/******************
 * Tin Can tools
 *******************/

// retruns an tincan object
function initTinCan()
{
	if(CONF["manual_registration"] == true)
	{
    var tincan = new TinCan (
    {
        recordStores: [
            {
                endpoint: CONF["endpoint"],
                username: CONF["tcusername"],
                password: CONF["tcpassword"],
                allowFail: false
            }
        ]
    }
    );
    return tincan
	}

	/** if LRS data is given by parameter **/
	var endpoint_str = getParameterByName("endpoint");
   	var auth_str = getParameterByName("auth");
   	console.log(auth_str);
	var tincan = new TinCan (
    {
            recordStores: [
            {
                endpoint:endpoint_str,
                auth: auth_str,
                allowFail: false
            }
        ]
    }
    );
    return tincan
}

// Calls when the users starts the project
function TinCanInit()
{
	var actor_obj = null;

	/** enter name manualy **/
    if(CONF["manual_registration"])
    {
		CONF["name"] = getParameterByName("name");
		CONF["email"] = getParameterByName("email");

		actor_obj = {
			mbox:CONF["email"],
			name:CONF["name"]
	 	   }
    }
    /** if not , get the parameters form the url **/
	else
	{
		actor_obj = JSON.parse(getParameterByName("actor"));
		console.log(actor_obj);
	}

    tc = initTinCan();
    tc.sendStatement(
	{
		actor:actor_obj,
	    verb:{
		id:"http://adlnet.gov/expapi/verbs/initialized",
	    "display":{"en-US":"Initialized","nb":"Startet"}},
	    target:{id:CONF["siteurl"],"definition":
		   {name:{"en-US":CONF["projectname"],
			  "nb":CONF["projectname"]}}}
	}
    );
}


// Calls when projects is complete and tincan option is set
var isSetComplete = false;
function TinCanComplete()
{
    if(isSetComplete){return;}

	var actor_obj = null;
	if(CONF["manual_registration"])
    {
		CONF["name"] = getParameterByName("name");
		CONF["email"] = getParameterByName("email");

		actor_obj = {
			mbox:CONF["email"],
			name:CONF["name"]
	 	   }
    }
    /** if not , get the parameters form the url **/
	else
	{
		actor_obj = JSON.parse(getParameterByName("actor"));
		console.log(actor_obj);
	}

    tc = initTinCan();
    tc.sendStatement(
	{
	    actor:actor_obj,
	    verb:{
		id:"http://adlnet.gov/expapi/verbs/completed",
	    "display":{"en-US":"Completed","nb":"Fullførte"}},
	    target:{id:CONF["siteurl"],"definition":
		   {name:{"en-US":CONF["projectname"],
			  "nb":CONF["projectname"]}}}
	}
    );
    isSetComplete = true;
    return se;
}
