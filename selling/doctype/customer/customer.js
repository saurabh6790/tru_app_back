// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

wn.require('app/setup/doctype/contact_control/contact_control.js');



cur_frm.add_fetch('division_head', 'address','division_head_address');


cur_frm.add_fetch('report_to', 'address','address');

cur_frm.add_fetch('report_to', 'short_name','short_name');

cur_frm.add_fetch('customer_group', 'parent_customer_group','master_group');

cur_frm.add_fetch('territory', 'parent_territory','main_territory');


cur_frm.cscript.onload = function(doc,dt,dn){
	cur_frm.cscript.load_defaults(doc, dt, dn);
}

cur_frm.cscript.load_defaults = function(doc, dt, dn) {
	doc = locals[doc.doctype][doc.name];
	if(!(doc.__islocal && doc.lead_name)) { return; }

	var fields_to_refresh = wn.model.set_default_values(doc);
	if(fields_to_refresh) { refresh_many(fields_to_refresh); }
}

cur_frm.add_fetch('lead_name', 'company_name', 'customer_name');
cur_frm.add_fetch('default_sales_partner','commission_rate','default_commission_rate');

cur_frm.cscript.refresh = function(doc, dt, dn) {
	cur_frm.cscript.setup_dashboard(doc);
	erpnext.hide_naming_series();

	if(doc.__islocal){		
		hide_field(['address_html','contact_html']);
	}else{		
		unhide_field(['address_html','contact_html']);
		// make lists
		cur_frm.cscript.make_address(doc,dt,dn,'address_html');
		cur_frm.cscript.make_contact(doc,dt,dn,'contact_html');

		cur_frm.cscript.make_address(doc,dt,dn,'division_address');
		cur_frm.cscript.make_contact(doc,dt,dn,'division_contact');

		cur_frm.communication_view = new wn.views.CommunicationList({
			parent: cur_frm.fields_dict.communication_html.wrapper,
			doc: doc,
		});
	}

	if(doc.__islocal){
		hide_field('dettach'); 
    
	}
  	else{
    	unhide_field('dettach');
  	}
}

cur_frm.cscript.setup_dashboard = function(doc) {
	cur_frm.dashboard.reset(doc);
	if(doc.__islocal) 
		return;
	if (in_list(user_roles, "Accounts User") || in_list(user_roles, "Accounts Manager"))
		cur_frm.dashboard.set_headline('<span class="text-muted">'+ wn._('Loading...')+ '</span>')
	
	cur_frm.dashboard.add_doctype_badge("Opportunity", "customer");
	cur_frm.dashboard.add_doctype_badge("Quotation", "customer");
	cur_frm.dashboard.add_doctype_badge("Sales Order", "customer");
	cur_frm.dashboard.add_doctype_badge("Delivery Note", "customer");
	cur_frm.dashboard.add_doctype_badge("Sales Invoice", "customer");
	
	return wn.call({
		type: "GET",
		method:"selling.doctype.customer.customer.get_dashboard_info",
		args: {
			customer: cur_frm.doc.name
		},
		callback: function(r) {
			if (in_list(user_roles, "Accounts User") || in_list(user_roles, "Accounts Manager")) {
				cur_frm.dashboard.set_headline(
					wn._("Total Billing This Year: ") + "<b>" 
					+ format_currency(r.message.total_billing, cur_frm.doc.default_currency)
					+ '</b> / <span class="text-muted">' + wn._("Unpaid") + ": <b>" 
					+ format_currency(r.message.total_unpaid, cur_frm.doc.default_currency) 
					+ '</b></span>');
			}
			cur_frm.dashboard.set_badge_count(r.message);
		}
	})
}

cur_frm.cscript.make_address = function(doc,cdt,cdn,address_html) {
	//alert(address_html)
	if(!cur_frm.address_list) {
		cur_frm.address_list = new wn.ui.Listing({
			parent: cur_frm.fields_dict[address_html].wrapper,
			page_length: 5,
			new_doctype: "Address",
			get_query: function() {
				return "select name, address_type, address_line1, address_line2, city, state, country, pincode, fax, email_id, phone, is_primary_address, is_shipping_address from tabAddress where customer='"+cur_frm.docname+"' and docstatus != 2 order by is_primary_address desc"
			},
			as_dict: 1,
			no_results_message: wn._('No addresses created'),
			render_row: cur_frm.cscript.render_address_row,
		});
		// note: render_address_row is defined in contact_control.js
	}
	cur_frm.address_list.run();
}

cur_frm.cscript.make_contact = function(doc,cdt,cdn,contact_html) {
	if(!cur_frm.contact_list) {
		cur_frm.contact_list = new wn.ui.Listing({
			parent: cur_frm.fields_dict[contact_html].wrapper,
			page_length: 5,
			new_doctype: "Contact",
			get_query: function() {
				return "select name, first_name, last_name, email_id, phone, mobile_no, department, designation, is_primary_contact from tabContact where customer='"+cur_frm.docname+"' and docstatus != 2 order by is_primary_contact desc"
			},
			as_dict: 1,
			no_results_message: wn._('No contacts created'),
			render_row: cur_frm.cscript.render_contact_row,
		});
		// note: render_contact_row is defined in contact_control.js
	}
	cur_frm.contact_list.run();

}

cur_frm.fields_dict['customer_group'].get_query = function(doc, dt, dn) {
	return{
		filters:{'is_group': 'No'}
	}
}


cur_frm.fields_dict.lead_name.get_query = function(doc, cdt, cdn) {
	return{
		query:"controllers.queries.lead_query"
	}
}

cur_frm.fields_dict['default_price_list'].get_query = function(doc, cdt, cdn) {
	return{
		filters:{'selling': 1}
	}
}

cur_frm.cscript.dettach = function(doc,cdt,cdn) {

	args={
    		"report_to":doc.report_to,
    		"date":doc.date,
    		"client":doc.customer_name
    	}
	return 	get_server_fields('get_new_reporting',JSON.stringify(args),'',doc,cdt,cdn,1);//,function(r,rt){refresh_field('training')});

}

cur_frm.cscript.report_to = function(doc,cdt,cdn) {
	return 	get_server_fields('get_today_date','','',doc,cdt,cdn,1);//,function(r,rt){refresh_field('training')});

	}




// cur_frm.cscript.report_to = function(doc,cdt,cdn){
// 	return get_server_fields('')
// }