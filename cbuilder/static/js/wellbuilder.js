/****************************************
 * Used for make bootstrap wells
 * A part of sitebuilder.js
 * 
 * @author Per-Henrik E. Kvalnes 2016
 ****************************************/

// selectedCol is defined by sitebuilder.js
function insertWell(data)
{
    var lData = false;
    
    // override popup from 
    popup = document.getElementById("popup");
    popup.innerHTML = "";

    div = document.createElement("div");
    div.className = "carpet";
    popup.appendChild(div);

    well_controllers = document.createElement("div");
    well_controllers.className = "well_controllers";
    div.appendChild(well_controllers);

    if(data.className == "well-column")
    {
	lData = true;
    }
    
    // append one instance of well with title
    nController = 0;
    function insertWellControllers(title, value)
    {
	if(lData == false){
	    title = i18n.t("builder.welltitle");
	    value = i18n.t("builder.welltext");
	}
	    
	// div tag to group title and text
	pair = document.createElement("div");
	pair.className = "well_pair";
	well_controllers.appendChild(pair);

	input_name = document.createElement("input");
	input_name.value = title;
	pair.appendChild(input_name);
	pair.appendChild(document.createElement("br"));
	area = document.createElement("textarea");
	area.value = value;
	area.id = "builder"+nController;
	
	pair.appendChild(area);
	pair.appendChild(document.createElement("hr"));

	if(lData == false){
	    tinymce.init(options);
	}
	
	nController += 1;
    }



    // add the well to the column
    function addWell()
    {
	wells = $(".well_pair");
	html = "<div class='well-column'>";
	id = generateRandomID();
	

	// add buttons
	html += "<div class='btn-group-justified'>";	
	for(i = 0; i < wells.length; i++)
	{
	    well = wells[i];
	    id_s = id+i;
	    html += "<p class='btn btn-primary well-button' id='"+id_s+"'>";
	    html += well.children[0].value + "</p>";
	}
	html +="</div>";

	// add wells
	for(i = 0; i < wells.length; i++)
	{
	    // use same ids as buttons but with a pre-fix (well)
	    id_s = 'well'+id+i;
	    well = wells[i];
	    html += "<div class='well well-lg' id='"+id_s+"' style='display:none'>";
	    html += tinymce.get("builder"+i).getContent();
	    html += "</div>";
	}
	html += "</div>";
	html += "</div>";
	console.log(html);
	selectedCol.innerHTML = html;
	$("#html_form")[0].value = slide.innerHTML;
	// remove the popup screen
	document.body.removeChild($("#popup")[0]);
	saveColumn();
    }

    // load data if there are some data given
    if(lData){
	var btn_grp = data.children[0];
	for(i = 0; i < btn_grp.children.length; i++)
	{
	    var btnid = btn_grp.children[i].id;
	    insertWellControllers( $("#"+btnid)[0].innerHTML,
				   $("#well"+btnid)[0].innerHTML);

	}
	lData = false;
    }
    else{
	insertWellControllers(i18n.t("builder.welltitle"),
			      i18n.t("builder.welltext"));
    }

    addwell = document.createElement("p");
    addwell.className = "btn btn-primary";
    addwell.innerHTML = i18n.t("builder.newwell");
    addwell.onclick = insertWellControllers;
    div.appendChild(addwell);

    submit = document.createElement("p");
    submit.className = "btn btn-primary";
    submit.innerHTML = i18n.t("builder.add");;
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
