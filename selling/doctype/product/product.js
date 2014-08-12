
// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



cur_frm.cscript.product_name = function(doc) {
	console.log("in the product_js");
	if(!doc.product_name) cur_frm.set_value("product_name", doc.product_name);
	if(!doc.description) cur_frm.set_value("description", doc.product_name);
}


cur_frm.cscript.validate = function(doc,cdt,cdn) {
	console.log("in the validate")
	cur_frm.cscript.update_totals(doc);
}

cur_frm.cscript.update_totals = function(doc) {
	console.log("in the update total");
	var td=0.0;
	var el = getchildren('Test Details', doc.name, 'test_details');
	for(var i in el) {
		console.log(el[i].test_rate)
		td += flt(el[i].test_rate,2);
		// tc += flt(el[i].credit, 2);
	}

	var doc = locals[doc.doctype][doc.name];
	doc.total_rate = td;
	console.log(doc.total_rate);
	refresh_many(['total_rate']);
}