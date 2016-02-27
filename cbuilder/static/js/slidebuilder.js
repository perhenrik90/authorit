/*******************************************
 * Slide edit
 *
 * @author Per-Henik Kvalnes - 2016
 ********************************************/
widgetCount = 0;


/************************
 * Create a column 
 ************************/
function createColumn(col_type)
{
    e = document.createElement("div");
    e.className = col_type;
    e.innerHTML = "text here";
    e.id = "wd"+widgetCount;
    e.onclick = editColumn;
    widgetCount += 1;
    return e;
}



function addRow(type="one")
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
}


/*******************************
 * Save one column and go back
 *******************************/

function saveColumn()
{
    edit = $("#edit")[0];
    console.log(edit.editon);
    
    col = $("#"+edit.editon)[0];
    col.innerHTML = tinymce.activeEditor.getContent()
    document.body.removeChild($("#popup")[0]);
    tinymce.remove();
}


/*********************************
 * Edit one column!
 *********************************/
function editColumn(id)
{
    col = this
    
    popup = document.createElement("div");
    popup.id = "popup";
    popup.className = "popup";
    document.body.appendChild(popup);

    save = document.createElement("div");
    save.className = "btn btn-primary";
    save.innerHTML = "Save";
    save.onclick = saveColumn;
    
    popup.appendChild(save);
    
    // create the text area
    tarea = document.createElement("textarea");
    tarea.id = "edit";
    tarea.editon = this.id;
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
