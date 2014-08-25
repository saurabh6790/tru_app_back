// // Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// // License: GNU General Public License v3. See license.txt

//wn.provide("erpnext.tour");

//cur_frm.add_fetch('client_name', 'address_html', 'address');

// $.extend(cur_frm.cscript, {
//     refresh:function(doc, cdt, cdn) {
//     	// console.log("in the refresh");
	
// 	if(doc.docstatus === 1) {
// 		cur_frm.add_custom_button(wn._('Tour Report'), cur_frm.cscript.create_report);
	
// 	}
// },

//     create_report:function() {
//   	console.log("in the js");
// 		wn.model.open_mapped_doc({
// 			method: "tour.doctype.tour_details.tour_details.create_report",
// 			source_name: cur_frm.doc.name
// 		})
// 	}

// });

cur_frm.cscript.refresh=function(doc,cdt,cdn){
  if(doc.docstatus == 1 ){
      cur_frm.add_custom_button(wn._('Create Tour Report'),
      cur_frm.cscript['Create Tour Report']);
   }
}

cur_frm.cscript['Create Tour Report'] = function() {

  wn.model.open_mapped_doc({
    method: "tour.doctype.tour_details.tour_details.create_report",
	source_name: cur_frm.doc.name
  })

}

cur_frm.cscript.validate = function(doc,cdt,cdn) {
	cur_frm.cscript.update_totals(doc);
}

cur_frm.cscript.client_name =function(doc,cdt,cdn){
	var d=locals[cdt][cdn];
	if(d.client_name){
	 //console.log(d.client_name)
   	get_server_fields('get_address',d.client_name, 'tour_client_details', doc, cdt, cdn, 1)
   	refresh_field('address');
	}
}

cur_frm.cscript.contact_person =function(doc,cdt,cdn){
	var d=locals[cdt][cdn];
	if(d.contact_person){
	 //console.log(d.client_name)
   	get_server_fields('get_contactno',d.contact_person, 'tour_client_details', doc, cdt, cdn, 1)
   	refresh_field('contact_no');
	}
}
cur_frm.cscript.update_totals = function(doc) {
	// console.log("in the update total");
	var td=0.0;
	var el = getchildren('Tour Client Details', doc.name, 'tour_client_details');
	for(var i in el) {
		td += flt(el[i].approx_advance_expense,2 );
		// tc += flt(el[i].credit, 2);
	}
	var doc = locals[doc.doctype][doc.name];
	doc.total_expenses = td;
	
	refresh_many(['total_expenses']);
}
