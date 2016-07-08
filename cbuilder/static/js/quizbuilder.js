/**********************************
 * Used for make simple quiz.
 * A part of sitebuilder.js
 * 
 * @author Per-Henrik E. Kvalnes 
 *********************************/

// selectedCol is defined by sitebuilder.js

function insertQuiz()
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
    div.appendChild(question);

    alternatives = document.createElement("div");
    div.appendChild(alternatives);
    
    var nAlternative = 1;
    function createAlternative()
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
	nAlternative ++;
    }
    createAlternative();
    createAlternative();



    
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
	saveColumn();
    }
    
    div.appendChild(document.createElement("hr"));

    add = document.createElement("p");
    add.innerHTML = i18n.t("builder.add");
    add.className = "btn btn-primary";
    add.onclick = addQuiz;
    div.appendChild(add);

    add = document.createElement("p");
    add.innerHTML = i18n.t("builder.createalternative");
    add.className = "btn btn-primary";
    add.onclick = createAlternative;
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
