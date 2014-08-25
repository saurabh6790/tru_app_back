// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.refresh=function(doc,cdt,cdn){
  if(doc.docstatus == 1) {
      cur_frm.add_custom_button(wn._('Create New Employee'),
      cur_frm.cscript['Create New Employee']);
   }

}
cur_frm.cscript['Create New Employee'] = function() {

  wn.model.open_mapped_doc({
    method: "job_application.doctype.job_application_form.job_application_form.create_new_employee",
    source_name: cur_frm.doc.name
  })

}


cur_frm.cscript.image = function() {
	refresh_field("image_view");
	
	if(!cur_frm.doc.description_html) {
		cur_frm.cscript.add_image(cur_frm.doc);
	} else {
		msgprint(wn._("You may need to update: ") + 
			wn.meta.get_docfield(cur_frm.doc.doctype, "description_html").label);
	}
}


cur_frm.cscript.add_image = function(doc, dt, dn) {
	if(!doc.image) {
		msgprint(wn._('Please select an "Image" first'));
		return;
	}

	doc.description_html = repl('<table style="width: 100%; table-layout: fixed;">'+
	'<tr><td style="width:110px"><img src="%(imgurl)s" width="100px"></td>'+
	'<td>%(desc)s</td></tr>'+
	'</table>', {imgurl: wn.utils.get_file_link(doc.image), desc:doc.description});

	refresh_field('description_html');
}