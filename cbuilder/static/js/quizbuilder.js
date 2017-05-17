/**********************************
 * Used for make simple quiz.
 * A part of sitebuilder.js
 * 
 * @author Per-Henrik E. Kvalnes 
 *********************************/

// selectedCol is defined by sitebuilder.js
function insertQuiz(data)
{
    // override popup from 
    popup = document.getElementById("popup");
    popup.innerHTML = "";

    div = document.createElement("div");
    div.className = "carpet";
    popup.appendChild(div);
   
    label = document.createElement("p");
    label.innerHTML = i18n.t("builder.enterquestion");
    div.appendChild(label);
    
    question  = document.createElement("input");
    question.id = "question";

    // if user is going to change the value
    if(data.className == "quiz_column"){
    	question.value = data.children[0].innerHTML;
    }
    div.appendChild(question);

    alternatives = document.createElement("div");
    div.appendChild(alternatives);

    //remove alternative
    function removeAlternative()
    {
    	alternatives.removeChild(this.parentNode);
    }

    // Create one alternative form row, and fill it with value
    var nAlternative = 1;
    function createAlternative(value)
    {
	alternative = document.createElement("div");
	alternative.className = "alternative";
	alternatives.appendChild(alternative);
	
	label = document.createElement("p");
	label.innerHTML = i18n.t("builder.alternative")+" "+nAlternative;

	
	alternative.appendChild(label)
	radio = document.createElement("input");
	radio.type = "checkbox";
	//radio.name = "right";
	radio.value = nAlternative;
	
	alternative.appendChild(radio);
	inn= document.createElement("input");
	alternative.appendChild(inn);
	if(typeof value != "object"){
	    inn.value = value;
	}

	remove = document.createElement("p");
	remove.className = "btn btn-danger";
	remove.innerHTML = i18n.t("builder.delete");
	remove.onclick = removeAlternative;
	alternative.appendChild(remove);
	
	nAlternative ++;
    }

    // if there are some data there, fill the form
    if(data.className == "quiz_column")
    {
	for(var i = 2; i < data.children.length; i ++){
    	    alternativ = data.children[i];
    	    createAlternative(alternativ.innerHTML);
	}
    }

    // if data do not exist, make two empty alternatives
    if(nAlternative == 1)
    {
	createAlternative(i18n.t("builder.alternative")+" "+1);
	createAlternative(i18n.t("builder.alternative")+" "+2);
    }
    
    // add the quiz to the column and close
    function addQuiz()
    {
	quiz_id = generateRandomID();
	
	html = "<div id='"+quiz_id+"' class='quiz_column'>";
	html += "<p>"+$("#question")[0].value+"</p>"
	html += "<hr/>";
	
	alternatives = $(".alternative");
	for(i = 0; i < alternatives.length; i ++)
	{
	    alt = alternatives[i];
	    console.log(alt.children[1].checked);

	    // add class true or false
	    html += "<p class='btn btn-primary "+alt.children[1].checked
		+" "+quiz_id+"' onclick='revealQuiz('"+quiz_id+"');'>"+alt.children[2].value;
	    html += "</p>";
	}
	html += "</div>";

	selectedCol.innerHTML = html;
	$("#html_form")[0].value = slide.innerHTML;
	// remove the popup screen
	document.body.removeChild($("#popup")[0]);
	//saveColumn();
	saveSlide();
    }
    
    div.appendChild(document.createElement("hr"));

    add = document.createElement("p");
    add.innerHTML = i18n.t("builder.createalternative");
    add.className = "btn btn-primary";
    add.onclick = createAlternative;
    div.appendChild(add);

    function clearColumn()
    {
	selectedCol.innerHTML = i18n.t("builder.texthere");
	$("#html_form")[0].value = slide.innerHTML;
	document.body.removeChild($("#popup")[0]);
	saveColumn();
    }
    
    clear = document.createElement("p");
    clear.innerHTML = i18n.t("builder.clearcolumn");
    clear.className = "btn btn-danger";
    clear.onclick = clearColumn;
    div.appendChild(clear);    

    div.appendChild( document.createElement("br"));
    add = document.createElement("p");
    add.innerHTML = i18n.t("builder.add");
    add.className = "btn btn-primary";
    add.onclick = addQuiz;
    div.appendChild(add);
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
