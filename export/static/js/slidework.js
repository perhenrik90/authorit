/************************************************
 * Slidework defines the framework for slides
 * Can be seen as the 'slide engine'.
 * 
 * @author Per-Henrik Kvalnes
 ***********************************************/


// used for configuration
CONF = {'manual_registration':false, 'siteurl':window.location, "projectname":'Test'}


// setup for all divtags with classname 'slide' 
function initSlideEngine()
{
    var se = new Object(); // define a slide engine
    var useTincan = false;
    var automode = false;
    
    // data objects / models
    se.slides = document.getElementsByClassName("slide");
    se.index = 0;

    // check if TinCan is used (uses tincan-min.js)
    if(window.location.search.indexOf("tincan=true")>0)
    {
	useTincan = true;
	console.log("Tincan / xAPI is turned on.");
	tincanStarted();
    }
   
    // updates the view 
    se.updateView = function()
    {
	// if not automatic mode, show next and prev buttons
	if(! automode)
	{
	    $('#nav-left').css("display","");
	    $('#nav-right').css("display","");
	}

	// loop through all slides and hide them and show the slide indexed
	for(var i = 0; i < se.slides.length; i ++)
	{
	    slide = se.slides[i];
	    slide.style.display = "none";
	    if(i == se.index)
	    {
		slide.style.display = "";
	    }
	}

	// Hide nextbutton if the user displays the last slide
	if(se.index == se.slides.length-1)
	{
	    $('#nav-right').css("display","None");
	}
	
	// Hide left button if first slide is in display
	if(se.index == 0)
	{
	    $('#nav-left').css("display","None");
	}


	
	// Update progress bar
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

	    
	    // if tincan is enabeled
	    if(useTincan)
	    {
		tincanComplete();
	    }
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


    }
    
    // set next button active
    se.enableNextButton = function()
    {
	nextbtn.className = "btn";
	nextbtn.onclick = se.nextSlide;
    }

    // check if auto-mode is turned on
    if(window.location.search.indexOf("automode=true")>0)
    {
	// hide next and preveus buttons
	automode = true;
	$("#nav-left").css("display","none");
	$("#nav-right").css("display","none");
	$("#navbar-header").css("display","none");
	
	// auto slide function
	function autoUpdate()
	{
	    if(se.index == se.slides.length-1)
	    {
		window.location = window.location;
	    }
	    else
	    {
		se.nextSlide();		
	    }
	}
	setInterval(autoUpdate, 60000);
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





/******************************************
 * Tin Can functions 
 ******************************************/

// initialice tincan
function setupTinCan()
{
    // get the parameters from url
    endpoint = getParameterByName("endpoint");

    // split the auth token based on base64
    auth = getParameterByName("auth");
    auth = auth.replace("Basic ","");
    auth = window.atob(auth);
    username = auth.split(":")[0].replace(" ","");
    password = auth.split(":")[1].replace(" ","");

    // create an tincan instance
    var tincan = new TinCan (
	{
            recordStores: [
		{
                    endpoint: endpoint,
                    username: username,
                    password: password,
                    allowFail: false
		}
            ]
	}
    );
    return tincan;
}


//
// Called when TinCan is enabeled and course is completed
//
function tincanComplete()
{
    var tincan = setupTinCan()

    // get actor object form url
    actor = getParameterByName("actor");
    actor = JSON.parse(actor);
    course_code = $("#course_code")[0].value;

    // set up the id (url) to this course
    act_id = "http://"+window.location.hostname+window.location.pathname
    title = document.title;

    // build the statement
    stm = { actor:actor,
            verb:{id:"http://adlnet.gov/expapi/verbs/completed",
		  display:{"en-EN":"Completed","nb":"Fullført"}
		 },
            object:{id:act_id,
                    definition:{name:{"en-US":title}},
                    description:{"en-US":"User has started the course: "+title}
                   },
          };
    tincan.sendStatement(stm);
}

//
// Called when TinCan is enabeled and couse is started
//
function tincanStarted()
{
    var tincan = setupTinCan()
    actor = getParameterByName("actor");
    actor = JSON.parse(actor);
    course_code = $("#course_code")[0].value;

    act_id = "http://"+window.location.hostname+window.location.pathname
    console.log(act_id);
    title = document.title;
    
    stm = { actor:actor,
            verb:{id:"http://adlnet.gov/expapi/verbs/started",
		  display:{"en-EN":"Started","nb":"Startet"}
		 },
            object:{id:act_id,
                    definition:{name:{"en-US":title}},
                    description:{"en-US":"User has started the course: "+title}
                   },
          };
    tincan.sendStatement(stm);
}

