/***********************************
 * Tool used with quizbuilder
 *
 * @author Per-Henrik Kvalnes 2016
 ***********************************/


function revealQuiz(id)
{
    $("."+id+".true").attr("class", "btn btn-success");
    $("."+id+".false").attr("class", "btn btn-danger");
    console.log(t);
}


// initialize the quiz buttons 
function initQuizes()
{
    quiz_columns = $(".quiz_column");

    for(var i = 0; i < quiz_columns.length; i ++)
    {
    	qc_id = quiz_columns[i].id;
	$(".btn."+qc_id).attr("onclick", "revealQuiz('"+qc_id+"')");
    }
}

initQuizes();
