/***********************************
 * Link builder
 *
 * @author Per-Henrik Kvalnes 2017
 ***********************************/

function insertLink(data){

    // override popup from 
    popup = document.getElementById("popup");
    popup.innerHTML = "";

    div = document.createElement("div");
    div.className = "carpet";
    popup.appendChild(div);

    function createSpan(name){
	span = document.createElement("span");
	span.innerHTML = name;
	return span;
    }

    
    label = document.createElement("p");
    label.innerHTML = i18n.t("builder.enterlink");
    div.appendChild(label);

    link_name = document.createElement("input");
    div.appendChild(link_name);
    div.appendChild(createSpan(i18n.t("builder.link_name")));
    div.appendChild( document.createElement("br"));

    url = document.createElement("input");
    div.appendChild(url);
    div.appendChild(createSpan(i18n.t("builder.url")));
    div.appendChild( document.createElement("br"));

    width = document.createElement("input");
    width.type = "number";
    width.min = "100";
    width.value = 400;
    div.appendChild(width);
    div.appendChild(createSpan(i18n.t("builder.width")));
    div.appendChild( document.createElement("br"));
    
    height = document.createElement("input");
    height.type = "number";
    height.min = "100";
    height.value = 800;
    div.appendChild(height);
    div.appendChild(createSpan(i18n.t("builder.height")));

    div.appendChild( document.createElement("hr"));

    function addLink(){
	link_id = generateRandomID();

	html = "<script> function "+link_id+"(){ window.open('"+url.value+"', '', 'width="+width.value+",height="+height.value+"');}</script>";
	html +="<p id="+link_id+" class='btn btn-primary' onclick='"+link_id+"()'>";
	html += link_name.value;
	html +="</p>";
	
	selectedCol.innerHTML = html;
	$("#html_form")[0].value = slide.innerHTML;
	// remove the popup screen
	document.body.removeChild($("#popup")[0]);
	//saveColumn();
	saveSlide();
    }

    submit = document.createElement("p");
    submit.innerHTML = i18n.t("builder.add");
    submit.className = "btn btn-primary";
    submit.onclick = addLink;
    div.appendChild(submit);
    
}
