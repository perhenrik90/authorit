/***********************************
 * Tool used with quizbuilder
 *
 * @author Per-Henrik Kvalnes 2016
 ***********************************/


function setWell(id)
{
    // hide all wells
    $(".well").css("display","none");
    // display well with 'well' -prefix based on button id
    $("#well"+this.id).css("display","");
}


// initialize the quiz buttons 
function initWells()
{
    well_buttons = $(".well-button");
    for(i = 0; i < well_buttons.length; i ++)
    {
	well_button = well_buttons[i];
	well_button.onclick = setWell;
    }
}
initWells();
