/*********************************
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
    label.innerHTML = "Enter question";
    div.appendChild(label);
    
    question  = document.createElement("input");
    question.id = "question";
    div.appendChild(question);

    var nAlternative = 1;
    function createAlternative()
    {
	alternative = document.createElement("div");
	alternative.className = "alternative";
	div.appendChild(alternative);
	
	label = document.createElement("p");
	label.innerHTML = "Alternative "+nAlternative;
	alternative.appendChild(label)
	radio = document.createElement("input");
	radio.type = "radio";
	radio.name = "right";
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
	html = "";
	html += "<p>"+$("#question")[0].value+"</p>"
	html += "<hr/>";
	
	alternatives = $(".alternative");
	for(i = 0; i < alternatives.length; i ++)
	{
	    alt = alternatives[i];
	    html += "<p class='btn btn-primary' value='"+alt.children[1].checked+"'>"+alt.children[2].value;
	    html += "</p>";
	}
	selectedCol.innerHTML = html;

	// remove the popup screen
	document.body.removeChild($("#popup")[0]);
    }
    
    div.appendChild(document.createElement("hr"));
    add = document.createElement("p");
    add.innerHTML = "Add";
    add.className = "btn btn-primary";
    add.onclick = addQuiz;
    div.appendChild(add);
}
