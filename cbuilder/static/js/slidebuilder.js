/*******************************************
 * Slide edit
 *
 * @author Per-Henik Kvalnes - 2016
 ********************************************/
var first = false;
var selectedCol = null;

/************************
 * Create a column 
 ************************/
function createColumn(col_type)
{
    if(first == 0)
    {
	widgetCount = $("#slide")[0].children.length;
    }
    e = document.createElement("div");
    e.className = col_type;
    e.innerHTML = "text here";
    e.id = "wd"+widgetCount;
    e.onclick = editColumn;
    widgetCount += 1;
    return e;
}



function addRow(type)
{
    slide = $("#slide")[0];

    new_row = document.createElement("div");
    new_row.className = "row";
    slide.appendChild(new_row);

    if(type == "one")
    {
	en1 = createColumn("col-sm-12");
	new_row.appendChild(en1);
    }
    if(type == "two")
    {
	en1 = createColumn("col-sm-6");
	new_row.appendChild(en1);
	en2 = createColumn("col-sm-6");
	new_row.appendChild(en2);
    }
    if(type == "three")
    {
	en1 = createColumn("col-sm-4");
	new_row.appendChild(en1);
	en2 = createColumn("col-sm-4");
	new_row.appendChild(en2);
	en3 = createColumn("col-sm-4");
	new_row.appendChild(en3);
    }
    if(type == "four")
    {
	en1 = createColumn("col-sm-3");
	new_row.appendChild(en1);
	en2 = createColumn("col-sm-3");
	new_row.appendChild(en2);
	en3 = createColumn("col-sm-3");
	new_row.appendChild(en3);
	en4 = createColumn("col-sm-3");
	new_row.appendChild(en4);
    }
    if(type == "smallbig")
    {
	en1 = createColumn("col-sm-4");
	new_row.appendChild(en1);
	en2 = createColumn("col-sm-8");
	new_row.appendChild(en2);
    }
    if(type == "bigsmall")
    {
	en1 = createColumn("col-sm-8");
	new_row.appendChild(en1);
	en2 = createColumn("col-sm-4");
	new_row.appendChild(en2);
    }
}


/*******************************
 * Save one column and go back
 *******************************/
function saveColumn()
{
    edit = $("#edit")[0];
    
    col = selectedCol;
    col.innerHTML = tinymce.activeEditor.getContent()
    document.body.removeChild($("#popup")[0]);
    tinymce.remove();

    // update the form to post the new view
    slide = $("#slide")[0];
    
    $("#html_form")[0].value = slide.innerHTML;
}


/*********************************
 * Edit one column!
 *********************************/
function editColumn()
{
    col = this
    selectedCol = this;
    console.log(col);
    popup = document.createElement("div");
    popup.id = "popup";
    popup.className = "popup";
    document.body.appendChild(popup);

    // Save button
    save = document.createElement("div");
    save.className = "glyphicon glyphicon-save btn btn-primary";
    save.innerHTML = "";
    save.onclick = saveColumn;
    popup.appendChild(save);

    // add image
    add_img = document.createElement("div");
    add_img.className = "glyphicon glyphicon glyphicon-picture btn btn-primary";
    add_img.innerHTML = "";
    add_img.onclick = insertImage;
    popup.appendChild(add_img);

    // add video
    add_vid = document.createElement("div");
    add_vid.className = "glyphicon glyphicon glyphicon-facetime-video btn btn-primary";
    add_vid.innerHTML = "";
    add_vid.onclick = insertVideo;
    popup.appendChild(add_vid);

    // add well
    add_vid = document.createElement("div");
    add_vid.className = "glyphicon glyphicon-text-background btn btn-primary";
    add_vid.innerHTML = "";
    add_vid.onclick = insertWell;
    popup.appendChild(add_vid);
    
    // add quiz
    add_vid = document.createElement("div");
    add_vid.className = "glyphicon glyphicon-question-sign btn btn-primary";
    add_vid.innerHTML = "";
    add_vid.onclick = insertQuiz;
    popup.appendChild(add_vid);
    
    // Delete row button
    delete_row = document.createElement("div");
    delete_row.className = "btn btn-danger glyphicon glyphicon-trash";

    delete_row.onclick = function(){
	var par = selectedCol.parentNode;
	slide = $("#slide")[0];
	slide.removeChild(par);
	saveColumn();
    }
    popup.appendChild(delete_row);

    
    // create the text area
    tarea = document.createElement("textarea");
    tarea.id = "edit";
   
    tarea.innerHTML = col.innerHTML;
    popup.appendChild(tarea);
    
    options = { selector: 'textarea',
		height: 500,
		plugins: [
		    'advlist autolink lists link image charmap print preview anchor',
		    'searchreplace visualblocks code fullscreen',
		    'insertdatetime media table contextmenu paste code', 'save'
		],
		toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
		content_css: [
		    '//fast.fonts.net/cssapi/e6dc9b99-64fe-4292-ad98-6974f93cd2a2.css',
		    '//www.tinymce.com/css/codepen.min.css'
		],
		theme_advanced_buttons3_add : "save",
		save_enablewhendirty : false,
		save_onsavecallback : "saveColumn"
	      }
    tinymce.init(options);
}



function insertImage()
{

    div = document.getElementById("popup");
    div.innerHTML = "";

    images_path = getImagePaths();

    // add image and close
    function selectImage(e)
    {
	tinymce.remove();
	selectedCol.innerHTML = "<img src='"+this.src+"' width='100%'></img>"
	$("#html_form")[0].value = slide.innerHTML;
	document.body.removeChild($("#popup")[0]);
    }
    
    for(i = 0; i < images_path.length; i ++)
    {
	img = document.createElement("img");
	img.style.width = "100px";
	img.src = images_path[i];
	img.onclick = selectImage;
	div.appendChild(img);
    }


}


function insertVideo()
{

    div = document.getElementById("popup");
    div.innerHTML = "";

    video_path = getVideoPaths();

    // add image and close
    function selectVideo(e)
    {
	var video_type = "video/mp4";

	if( this.src.indexOf('.ogg') > -1){ video_type = "video/ogg"}
	if( this.src.indexOf('.ogv') > -1){ video_type = "video/ogg"}

	    
	selectedCol.innerHTML = "<video src='"+this.src+"' type='"+video_type+"' width='100%' controls ></video>"
	$("#html_form")[0].value = slide.innerHTML;
	document.body.removeChild($("#popup")[0]);
    }
    
    for(i = 0; i < video_path.length; i ++)
    {
	video = document.createElement("video");
	video.style.width = "100px";
	video.type = "video/ogg";
	video.src = video_path[i];
	video.onclick = selectVideo;
	div.appendChild(video);
    }


}
