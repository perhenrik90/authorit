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
    popup.appendChild(div);
    
    label = document.createElement("p");
    label.innerHTML = "Enter question";
    div.appendChild(label);
    
    question  = document.createElement("input");
    div.appendChild(question);
}
