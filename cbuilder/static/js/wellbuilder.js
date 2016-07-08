/****************************************
 * Used for make bootstrap wells
 * A part of sitebuilder.js
 * 
 * @author Per-Henrik E. Kvalnes 2016
 ****************************************/

// selectedCol is defined by sitebuilder.js
function insertWell()
{
    // override popup from 
    popup = document.getElementById("popup");
    popup.innerHTML = "";

    div = document.createElement("div");
    div.className = "carpet";
    popup.appendChild(div);

    well_controllers = document.createElement("div");
    well_controllers.className = "well_controllers";
    div.appendChild(well_controllers);
    
    // append one instance of well with title
    function insertWellControllers()
    {
	pair = document.createElement("div");
	pair.className = "well_pair";
	well_controllers.appendChild(pair);

	input_name = document.createElement("input");
	pair.appendChild(input_name);
	pair.appendChild(document.createElement("br"));
	area = document.createElement("textarea");
	pair.appendChild(area);
	pair.appendChild(document.createElement("hr"));
    }
    insertWellControllers();


    // add the well to the column
    function addWell()
    {
	wells = $(".well_pair");
	html = "";
	id = generateRandomID();
	if(wells.length == 1)
	{
	    well = wells[0];
	    console.log(well);
	    html += "<div class='well well-lg'>";
	    html += well.children[2].value;
	    html += "</div>";

	    selectedCol.innerHTML = html;
	    $("#html_form")[0].value = slide.innerHTML;

	    // remove the popup screen
	    document.body.removeChild($("#popup")[0]);
	    saveColumn();
	    return;
	}

	// add buttons
	for(i = 0; i < wells.length; i++)
	{
	    well = wells[i];
	    id_s = id+i;
	    html += "<p class='btn btn-primary well-button' id='"+id_s+"'>";
	    html += well.children[0].value + "</p>";
	}

	// add wells
	for(i = 0; i < wells.length; i++)
	{
	    // use same ids as buttons but with a pre-fix (well)
	    id_s = 'well'+id+i;
	    well = wells[i];
	    html += "<div class='well well-lg' id='"+id_s+"' style='display:none'>";
	    html += well.children[2].value;
	    html += "</div>";
	}


	selectedCol.innerHTML = html;
	$("#html_form")[0].value = slide.innerHTML;
	// remove the popup screen
	document.body.removeChild($("#popup")[0]);
	saveColumn();

    }

    addwell = document.createElement("p");
    addwell.className = "btn btn-primary";
    addwell.innerHTML = "New well";
    addwell.onclick = insertWellControllers;
    div.appendChild(addwell);
    

    submit = document.createElement("p");
    submit.className = "btn btn-primary";
    submit.innerHTML = "Add";
    submit.onclick = addWell;
    div.appendChild(submit);
}







/************************
 * Generate a random ID
 ************************/
function generateRandomID()
{
    var possible = "abcdefghklmnq";
    var rnd = "";
    var run = true;

    while(run)
    {
	for(i = 0; i < 10; i ++)
	{
	    rnd += possible.charAt(Math.floor(Math.random() * possible.length));
	}
	if($(rnd).length == 0)
	{
	    run = false;
	}
    }
    return rnd;
}
