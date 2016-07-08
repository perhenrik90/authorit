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
	for(i = 0; i < wells.length; i++)
	{
	    well = wells[i];
	    console.log(well);
	    html += "<div class='well well-lg'>";
	    html += well.children[2].value;
	    html += "</div>";
	}


	selectedCol.innerHTML = html;
	$("#html_form")[0].value = slide.innerHTML;
	// remove the popup screen
	document.body.removeChild($("#popup")[0]);
	saveColumn();

    }
    

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
