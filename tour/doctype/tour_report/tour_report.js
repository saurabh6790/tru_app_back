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

cur_frm.cscript.date = function(doc,cdt,cdn){
	var d= locals[cdt][cdn];
	console.log("in date trigger");
	if((d.date <= doc.to_date && d.date >= doc.from_date)){
		//console.log("ok");
	} 
	else{
		msgprint("Mentioned Date must be between From Date & To Date");
	}
}