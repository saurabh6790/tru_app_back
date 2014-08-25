cur_frm.cscript.validate = function(doc,cdt,cdn) {
	cur_frm.cscript.update_totals(doc);
}

cur_frm.cscript.update_totals = function(doc) {
	console.log("in the update total");
	var td=0.0;
	var el = getchildren('Tour Daily Report', doc.name, 'tour_daily_report');
	for(var i in el) {
		td += flt(el[i].expense_incurred,2 );
		// tc += flt(el[i].credit, 2);
	}
	var doc = locals[doc.doctype][doc.name];
	doc.total_expenses = td;
	
	refresh_many(['total_expenses']);
}