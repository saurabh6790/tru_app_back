// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.refresh = function(doc,cdt,cdn){
	 if(doc.docstatus == 1) {
      	cur_frm.add_custom_button(wn._('Make Quotation'),
      		cur_frm.cscript['Make Quotation']);
   }

}


//Make Tender
//=====================================================================================

cur_frm.cscript['Make Quotation'] = function() {
	wn.model.open_mapped_doc({
		method: "selling.doctype.tender.tender.make_quotation",
		source_name: cur_frm.doc.name
	})
}