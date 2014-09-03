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


cur_frm.cscript.opening_date = function(doc,cdt,cdn){
	if (doc.submission_date){
		if (doc.opening_date<=doc.submission_date)
			console.log("ok");
		else
			msgprint("Opening date of tender must be less than the submission date of tender");
	}
}

cur_frm.cscript.submission_date = function(doc,cdt,cdn){
	if(doc.opening_date){
		if(doc.opening_date<=doc.submission_date)
			console.log("ok");
		else
			msgprint("Submission Date of tender must be greater than the opening date of tender");
	}
}

cur_frm.cscript.estimated_cost = function(doc,cdt,cdn){
	if(doc.estimated_cost<=0)
		msgprint("Estimated cost of the tender must be gretaer then zero");
}