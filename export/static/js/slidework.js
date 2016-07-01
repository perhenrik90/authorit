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
		//setCourseComplete();
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





//
function setupTinCan()
{
    var tincan = new TinCan (
	{
            recordStores: [
		{
                    endpoint: "http://lrstest.helsenord.no/data/xAPI/",
                    username: "b082cf4d6202ece29b637d6b2386712621c36c1c",
                    password: "02c97d2ca5c2fd5e8e0a4d9a7ab9f1d57a6824b2",
                    allowFail: false
		}
            ]
	}
    );
    return tincan;
}

function tincanStarted()
{
    var tincan = setupTinCan()
    actor = getParameterByName("actor");
    actor = JSON.parse(actor);

    id = String( window.location );
    title = document.title;
    
    stm = { actor:actor,
            verb:{id:"http://adlnet.gov/expapi/verbs/attempted",
		  display:{"en-EN":"Attempted","nb":"Startet"}
		 },
            object:{id:"act:authorit",
                    definition:{name:{"en-US":title}},
                    description:{"en-US":"User has started the course: "+title}
                   },
          };
    tincan.sendStatement(stm);
}

