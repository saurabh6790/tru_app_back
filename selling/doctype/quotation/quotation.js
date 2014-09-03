// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// Module CRM
// =====================================================================================
cur_frm.cscript.tname = "Quotation Item";
cur_frm.cscript.fname = "quotation_details";
cur_frm.cscript.other_fname = "other_charges";
cur_frm.cscript.sales_team_fname = "sales_team";

wn.require('app/accounts/doctype/sales_taxes_and_charges_master/sales_taxes_and_charges_master.js');
wn.require('app/utilities/doctype/sms_control/sms_control.js');
wn.require('app/selling/sales_common.js');
wn.require('app/accounts/doctype/sales_invoice/pos.js');


cur_frm.add_fetch('item_code', 'product_test_details','test_details');


erpnext.selling.QuotationController = erpnext.selling.SellingController.extend({
	onload: function(doc, dt, dn) {
		var me = this;
		this._super(doc, dt, dn);
		if(doc.customer && !doc.quotation_to)
			doc.quotation_to = "Customer";
		else if(doc.lead && !doc.quotation_to)
			doc.quotation_to = "Lead";

		// to overwrite the customer_filter trigger from queries.js
		if (doc.lead) {
			$.each(["customer_address", "shipping_address_name"], 
				function(i, opts) {
					me.frm.set_query(opts, erpnext.queries["lead_filter"]);
				}
			);
		}
	},
	refresh: function(doc, dt, dn) {
		this._super(doc, dt, dn);
		// if(doc.docstatus == 1 && doc.status!=='Lost' && doc.tender_name==null)
		// 	cur_frm.add_custom_button(wn._('Make Tender'), 
		// 		cur_frm.cscript['Make Tender']);
		if(doc.docstatus == 1 && doc.status!=='Lost') {
			cur_frm.add_custom_button(wn._('Make Regular Sales Order'), 
				cur_frm.cscript['Make Regular Sales Order']);
			cur_frm.add_custom_button(wn._('Make Provisional Sales Order'), 
				cur_frm.cscript['Make Provisional Sales Order']);
			if(doc.status!='Negotiation Mode' && doc.status!='Ordered')

				cur_frm.add_custom_button(wn._('Set As Negotiation Mode'), 
					cur_frm.cscript['Set As Negotiation Mode'], "icon-exclamation");
			if(doc.status!=="Ordered") {
				cur_frm.add_custom_button(wn._('Set as Lost'), 
					cur_frm.cscript['Declare Order Lost'], "icon-exclamation");
			}
			cur_frm.appframe.add_button(wn._('Send SMS'), cur_frm.cscript.send_sms, "icon-mobile-phone");
		}
		
		if (this.frm.doc.docstatus===0) {
			cur_frm.add_custom_button(wn._('From Opportunity'), 
				function() {
					wn.model.map_current_doc({
						method: "selling.doctype.opportunity.opportunity.make_quotation",
						source_doctype: "Opportunity",
						get_query_filters: {
							docstatus: 1,
							status: "Submitted",
							enquiry_type: cur_frm.doc.order_type,
							customer: cur_frm.doc.customer || undefined,
							lead: cur_frm.doc.lead || undefined,
							company: cur_frm.doc.company
						}
					})
				});
		}

		if (!doc.__islocal) {
			cur_frm.communication_view = new wn.views.CommunicationList({
				list: wn.model.get("Communication", {"parent": doc.name, "parenttype": "Quotation"}),
				parent: cur_frm.fields_dict.communication_html.wrapper,
				doc: doc,
				recipients: doc.contact_email
			});
		}
		
		this.quotation_to();
	},
	
	quotation_to: function() {
		this.frm.toggle_reqd("lead", this.frm.doc.quotation_to == "Lead");
		this.frm.toggle_reqd("customer", this.frm.doc.quotation_to == "Customer");
		if (this.frm.doc.quotation_to == "Lead") {
			this.frm.set_value("customer", null);
			this.frm.set_value("contact_person", null);
		}
		else if (this.frm.doc.quotation_to == "Customer")
			this.frm.set_value("lead", null);
	},

	tc_name: function() {
		this.get_terms();
	},
	
	validate_company_and_party: function(party_field) {
		if(!this.frm.doc.quotation_to) {
			msgprint(wn._("Please select a value for" + " " + wn.meta.get_label(this.frm.doc.doctype,
				"quotation_to", this.frm.doc.name)));
			return false;
		} else if (this.frm.doc.quotation_to == "Lead") {
			return true;
		} else {
			return this._super(party_field);
		}
	},
});

cur_frm.script_manager.make(erpnext.selling.QuotationController);

cur_frm.fields_dict.lead.get_query = function(doc, cdt, cdn) {
	return{	query:"controllers.queries.lead_query" } }

cur_frm.cscript.lead = function(doc, cdt, cdn) {
	if(doc.lead) {
		unhide_field('territory');
		return cur_frm.call({
			doc: cur_frm.doc,
			method: "set_lead_defaults",
			callback: function(r) {
				if(!r.exc) {
					cur_frm.refresh_fields();
				}
			}
		});
	}
}


// Make Sales Order
// =====================================================================================
cur_frm.cscript['Make Regular Sales Order'] = function() {
	wn.model.open_mapped_doc({
		method: "selling.doctype.quotation.quotation.make_sales_order",
		source_name: cur_frm.doc.name
	})
}

// Make Provisional Sales Order
// =====================================================================================
cur_frm.cscript['Make Provisional Sales Order'] = function() {
	wn.model.open_mapped_doc({
		method: "selling.doctype.quotation.quotation.make_provisional_sales_order",
		source_name: cur_frm.doc.name
	})
}

// // Make Non Provisional Sales Order
// // =====================================================================================
// cur_frm.cscript['Make  Non Provisional Sales Order'] = function() {
// 	wn.model.open_mapped_doc({
// 		method: "selling.doctype.quotation.quotation.make_non_provisional_sales_order",
// 		source_name: cur_frm.doc.name
// 	})
// }

// Make Sales Invoice
// =====================================================================================
cur_frm.cscript['Make Sales Invoice'] = function() {
	wn.model.open_mapped_doc({
		method: "selling.doctype.quotation.quotation.make_sales_invoice",
		source_name: cur_frm.doc.name
	})
}

// Make Tender
// =====================================================================================
// cur_frm.cscript['Make Tender'] = function() {
// 	wn.model.open_mapped_doc({
// 		method: "selling.doctype.quotation.quotation.make_tender",
// 		source_name: cur_frm.doc.name
// 	})
// }

// // Make Negotiation Mode
// // =====================================================================================
// cur_frm.cscript['Set As Negotiation Mode'] = function() {
// 	console.log("nnnnn");
// 	wn.model.open_mapped_doc({
// 		method: "selling.doctype.quotation.quotation.set_as_negotiation_mode",
// 		source_name: cur_frm.doc.name
// 	})
// }


// declare order lost
//-------------------------
cur_frm.cscript['Declare Order Lost'] = function(){
	var dialog = new wn.ui.Dialog({
		title: "Set As Lost",
		fields: [
			{"fieldtype": "Text", "label": wn._("Reason For Losing"), "fieldname": "reason",
				"reqd": 1 },
			{"fieldtype": "Button", "label": wn._("Update"), "fieldname": "update"},
		]
	});

	dialog.fields_dict.update.$input.click(function() {
		args = dialog.get_values();
		if(!args) return;
		return cur_frm.call({
			method: "declare_order_lost",
			doc: cur_frm.doc,
			args: args.reason,
			callback: function(r) {
				if(r.exc) {
					msgprint(wn._("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
	
}


//Make Negotiation Mode
//=====================================================================================

cur_frm.cscript['Set As Negotiation Mode'] = function(){
	var dialog = new wn.ui.Dialog({
		title: "Set As Negotiation Mode",
		fields: [
			{"fieldtype": "Text", "label": wn._("Reason For Negotiation"), "fieldname": "n_reason",
				"reqd": 1 },
			{"fieldtype": "Button", "label": wn._("Done"), "fieldname": "update"},
		]
	});

	dialog.fields_dict.update.$input.click(function() {
		args = dialog.get_values();
		if(!args) return;
		return cur_frm.call({
			method: "declare_order_negotiated",
			doc: cur_frm.doc,
			//args: 'Negotiation Mode'
			callback: function(r) {
				if(r.exc) {
					msgprint(wn._("There were errors."));
					return;
				}
				dialog.hide();
				cur_frm.refresh();
			},
			btn: this
		})
	});
	dialog.show();
	
}


cur_frm.cscript.on_submit = function(doc, cdt, cdn) {
	if(cint(wn.boot.notification_settings.quotation))
		cur_frm.email_doc(wn.boot.notification_settings.quotation_message);
}



// cur_frm.cscript.validate = function(doc,cdt,cdn) {
// 	// console.log("in the validate")
// 	cur_frm.cscript.update_totals(doc);
// }

// cur_frm.cscript.update_totals = function(doc, cdt, cdn) {
// 	// console.log("in the validate");
// 	var td=0.0;
// 	var el = getchildren('Quotation Product', doc.name, 'quotation_product');
// 	console.log(el);
// 	for(var i in el) {
// 		console.log(el[i].total_rate)
// 		td += flt(el[i].total_rate,2);
// 		// tc += flt(el[i].credit, 2);
// 	}

// 	var doc = locals[doc.doctype][doc.name];
// 	doc.net_total_export = td;
// 	console.log(doc.net_total_export);
// 	refresh_many(['net_total_export']);
// }



