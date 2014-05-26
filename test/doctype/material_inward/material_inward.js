


// On Refresh add Button Make Stock Entry- Material Transfer
cur_frm.cscript.refresh = function(doc){

	if(doc.docstatus==1) {
		cur_frm.add_custom_button(wn._('Make Stock Entry- Material Transfer'), 
				cur_frm.cscript['Make Stock Entry- Material Transfer']);
	}

}


// For Calling Method From Py File.
cur_frm.cscript['Make Stock Entry- Material Transfer'] = function() {
	wn.model.open_mapped_doc({
		method: "test.doctype.material_inward.material_inward.make_material_transfer",
		source_name: cur_frm.doc.name
	})
}		