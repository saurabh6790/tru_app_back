// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.cscript.tname = "Stock Entry Detail";
cur_frm.cscript.fname = "mtn_details";

wn.require("public/app/js/controllers/stock_controller.js");
wn.provide("erpnext.stock");

cur_frm.add_fetch('client_company', 'address', 'company_address');

cur_frm.add_fetch('electronically_approved_by_1', 'first_name', 'approver_1_name');

cur_frm.add_fetch('electronically_approved_by_2', 'first_name', 'approver_2_name');

erpnext.stock.StockEntry = erpnext.stock.StockController.extend({		
	setup: function() {
		var me = this;
		
		this.frm.fields_dict.delivery_note_no.get_query = function() {
			return { query: "stock.doctype.stock_entry.stock_entry.query_sales_return_doc" };
		};
		
		this.frm.fields_dict.sales_invoice_no.get_query = 
			this.frm.fields_dict.delivery_note_no.get_query;
		
		this.frm.fields_dict.purchase_receipt_no.get_query = function() {
			return { 
				filters:{ 'docstatus': 1 }
			};
		};
		
		this.frm.fields_dict.mtn_details.grid.get_field('item_code').get_query = function() {
			if(in_list(["Sales Return", "Purchase Return"], me.frm.doc.purpose) && 
				me.get_doctype_docname()) {
					return {
						query: "stock.doctype.stock_entry.stock_entry.query_return_item",
						filters: {
							purpose: me.frm.doc.purpose,
							delivery_note_no: me.frm.doc.delivery_note_no,
							sales_invoice_no: me.frm.doc.sales_invoice_no,
							purchase_receipt_no: me.frm.doc.purchase_receipt_no
						}
					};
			} else {
				return erpnext.queries.item({is_stock_item: "Yes"});
			}
		};
		
		if(cint(wn.defaults.get_default("auto_accounting_for_stock"))) {
			this.frm.add_fetch("company", "stock_adjustment_account", "expense_account");
			this.frm.fields_dict.mtn_details.grid.get_field('expense_account').get_query = 
					function() {
				return {
					filters: { 
						"company": me.frm.doc.company,
						"group_or_ledger": "Ledger"
					}
				}
			}
		}
	},
	
	onload_post_render: function() {
		this.set_default_account();
	},
	
	refresh: function() {
		var me = this;
		erpnext.hide_naming_series();
		this.toggle_related_fields(this.frm.doc);
		this.toggle_enable_bom();
		this.show_stock_ledger();
		this.show_general_ledger();

		//add button make outward register
		if(this.frm.doc.docstatus==1 && this.frm.doc.internal_purpose=='Inward')
			this.frm.add_custom_button(wn._("Make Sample Entry"), function() { me.make_sample_entry(); });
		
		// if(this.frm.doc.docstatus==1 && this.frm.doc.purpose=='Material Transfer' && this.frm.doc.material_inward!=null && this.frm.doc.sample_generated!='Yes')
		// 	this.frm.add_custom_button(wn._("Make Sample Id"), function() { me.make_sample_id(); });
		
		if(this.frm.doc.docstatus === 1 && 
				wn.boot.profile.can_create.indexOf("Journal Voucher")!==-1) {
			if(this.frm.doc.purpose === "Sales Return") {
				this.frm.add_custom_button(wn._("Make Credit Note"), function() { me.make_return_jv(); });
				this.add_excise_button();
			} else if(this.frm.doc.purpose === "Purchase Return") {
				this.frm.add_custom_button(wn._("Make Debit Note"), function() { me.make_return_jv(); });
				this.add_excise_button();
			}
		}
		
	},
	
	on_submit: function() {
		this.clean_up();
	},
	
	after_cancel: function() {
		this.clean_up();
	},

	set_default_account: function() {
		var me = this;
		
		if(cint(wn.defaults.get_default("auto_accounting_for_stock"))) {
			var account_for = "stock_adjustment_account";
			if (this.frm.doc.purpose == "Sales Return")
				account_for = "stock_in_hand_account";
			else if (this.frm.doc.purpose == "Purchase Return") 
				account_for = "stock_received_but_not_billed";
			
			return this.frm.call({
				method: "accounts.utils.get_company_default",
				args: {
					"fieldname": account_for, 
					"company": this.frm.doc.company
				},
				callback: function(r) {
					if (!r.exc) {
						for(d in getchildren('Stock Entry Detail', me.frm.doc.name, 'mtn_details')) {
							if(!d.expense_account) d.expense_account = r.message;
						}
					}
				}
			});
		}
	},
	
	clean_up: function() {
		// Clear Production Order record from locals, because it is updated via Stock Entry
		if(this.frm.doc.production_order && 
				this.frm.doc.purpose == "Manufacture/Repack") {
			wn.model.remove_from_locals("Production Order", 
				this.frm.doc.production_order);
		}
	},
	
	get_items: function() {
		if(this.frm.doc.production_order || this.frm.doc.bom_no) {
			// if production order / bom is mentioned, get items
			return this.frm.call({
				doc: this.frm.doc,
				method: "get_items",
				callback: function(r) {
					if(!r.exc) refresh_field("mtn_details");
				}
			});
		}
	},
	
	qty: function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		d.transfer_qty = flt(d.qty) * flt(d.conversion_factor);
		refresh_field('mtn_details');
	},
	
	production_order: function() {
		var me = this;
		this.toggle_enable_bom();
		
		return this.frm.call({
			method: "get_production_order_details",
			args: {production_order: this.frm.doc.production_order},
			callback: function(r) {
				if (!r.exc) {
					if (me.frm.doc.purpose == "Material Transfer" && !me.frm.doc.to_warehouse)
						me.frm.set_value("to_warehouse", r.message["wip_warehouse"]);
				}
			}
		});
	},
	
	toggle_enable_bom: function() {
		this.frm.toggle_enable("bom_no", !this.frm.doc.production_order);
	},
	
	get_doctype_docname: function() {
		if(this.frm.doc.purpose === "Sales Return") {
			if(this.frm.doc.delivery_note_no && this.frm.doc.sales_invoice_no) {
				// both specified
				msgprint(wn._("You can not enter both Delivery Note No and Sales Invoice No. \
					Please enter any one."));
				
			} else if(!(this.frm.doc.delivery_note_no || this.frm.doc.sales_invoice_no)) {
				// none specified
				msgprint(wn._("Please enter Delivery Note No or Sales Invoice No to proceed"));
				
			} else if(this.frm.doc.delivery_note_no) {
				return {doctype: "Delivery Note", docname: this.frm.doc.delivery_note_no};
				
			} else if(this.frm.doc.sales_invoice_no) {
				return {doctype: "Sales Invoice", docname: this.frm.doc.sales_invoice_no};
				
			}
		} else if(this.frm.doc.purpose === "Purchase Return") {
			if(this.frm.doc.purchase_receipt_no) {
				return {doctype: "Purchase Receipt", docname: this.frm.doc.purchase_receipt_no};
				
			} else {
				// not specified
				msgprint(wn._("Please enter Purchase Receipt No to proceed"));
				
			}
		}
	},
	
	add_excise_button: function() {
		if(wn.boot.control_panel.country === "India")
			this.frm.add_custom_button(wn._("Make Excise Invoice"), function() {
				var excise = wn.model.make_new_doc_and_get_name('Journal Voucher');
				excise = locals['Journal Voucher'][excise];
				excise.voucher_type = 'Excise Voucher';
				loaddoc('Journal Voucher', excise.name);
			});
	},
	
	make_return_jv: function() {
		if(this.get_doctype_docname()) {
			return this.frm.call({
				method: "make_return_jv",
				args: {
					stock_entry: this.frm.doc.name
				},
				callback: function(r) {
					if(!r.exc) {
						var jv_name = wn.model.make_new_doc_and_get_name('Journal Voucher');
						var jv = locals["Journal Voucher"][jv_name];
						$.extend(jv, r.message[0]);
						$.each(r.message.slice(1), function(i, jvd) {
							var child = wn.model.add_child(jv, "Journal Voucher Detail", "entries");
							$.extend(child, jvd);
						});
						loaddoc("Journal Voucher", jv_name);
					}
				}
			});
		}
	},

	//for calling method form py file
	make_sample_entry: function() {
		wn.model.open_mapped_doc({
			method: "stock.doctype.stock_entry.stock_entry.make_sample_entry",
			source_name: cur_frm.doc.name

		})
	},

	// make_sample_id: function() {
	// 	wn.model.open_mapped_doc({
	// 		method: "stock.doctype.stock_entry.stock_entry.make_sample_id",
	// 		source_name: cur_frm.doc.name
	// 		// args: {
	// 		// 		"source_name": cur_frm.doc.name, 
	// 		// 		"material": cur_frm.doc.material_inward
	// 		// 	},
	// 	})
	// },

	mtn_details_add: function(doc, cdt, cdn) {
		var row = wn.model.get_doc(cdt, cdn);
		this.frm.script_manager.copy_from_first_row("mtn_details", row, 
			["expense_account", "cost_center"]);
		
		if(!row.s_warehouse) row.s_warehouse = this.frm.doc.from_warehouse;
		if(!row.t_warehouse) row.t_warehouse = this.frm.doc.to_warehouse;
	},
	
	mtn_details_on_form_rendered: function(doc, grid_row) {
		erpnext.setup_serial_no(grid_row)
	}
});

cur_frm.script_manager.make(erpnext.stock.StockEntry);

cur_frm.cscript.toggle_related_fields = function(doc) {
	disable_from_warehouse = inList(["Material Receipt", "Sales Return"], doc.purpose);
	disable_to_warehouse = inList(["Material Issue", "Purchase Return"], doc.purpose);
	
	disable_posting_date = inList(["Inward","Outward"],doc.internal_purpose);
	cur_frm.toggle_enable("posting_date",!disable_posting_date);

	cur_frm.toggle_enable("from_warehouse", !disable_from_warehouse);
	cur_frm.toggle_enable("to_warehouse", !disable_to_warehouse);
		
	cur_frm.fields_dict["mtn_details"].grid.set_column_disp("s_warehouse", !disable_from_warehouse);
	cur_frm.fields_dict["mtn_details"].grid.set_column_disp("t_warehouse", !disable_to_warehouse);
	//cur_frm.fields_dict["mtn_details"].grid.set_column_disp("batch_no",!disable_batch_no);
	if(doc.internal_purpose == 'Outward'){
		cur_frm.set_value('from_warehouse','Work In Progress - TF')
		cur_frm.set_value('to_warehouse','Stores - TF')
		refresh_field('from_warehouse')
		refresh_field('to_warehouse')
	}
	if(doc.internal_purpose == 'Inward'){
		cur_frm.set_value('from_warehouse','Stores - TF')
		cur_frm.set_value('to_warehouse','Work In Progress - TF')
		refresh_field('from_warehouse')
		refresh_field('to_warehouse')
	}
	if(doc.purpose == 'Purchase Return') {
		doc.customer = doc.customer_name = doc.customer_address = 
			doc.delivery_note_no = doc.sales_invoice_no = null;
		doc.bom_no = doc.production_order = doc.fg_completed_qty = null;
	} else if(doc.purpose == 'Sales Return') {
		doc.supplier=doc.supplier_name = doc.supplier_address = doc.purchase_receipt_no=null;
		doc.bom_no = doc.production_order = doc.fg_completed_qty = null;
	} else {
		doc.customer = doc.customer_name = doc.customer_address = 
			doc.delivery_note_no = doc.sales_invoice_no = doc.supplier = 
			doc.supplier_name = doc.supplier_address = doc.purchase_receipt_no = null;
	}
}

cur_frm.cscript.delivery_note_no = function(doc, cdt, cdn) {
	if(doc.delivery_note_no)
		return get_server_fields('get_cust_values', '', '', doc, cdt, cdn, 1);
}

cur_frm.cscript.sales_invoice_no = function(doc, cdt, cdn) {
	if(doc.sales_invoice_no) 
		return get_server_fields('get_cust_values', '', '', doc, cdt, cdn, 1);
}

cur_frm.cscript.customer = function(doc, cdt, cdn) {
	if(doc.customer) 
		return get_server_fields('get_cust_addr', '', '', doc, cdt, cdn, 1);
}

cur_frm.cscript.purchase_receipt_no = function(doc, cdt, cdn) {
	if(doc.purchase_receipt_no)	
		return get_server_fields('get_supp_values', '', '', doc, cdt, cdn, 1);
}

cur_frm.cscript.supplier = function(doc, cdt, cdn) {
	if(doc.supplier) 
		return get_server_fields('get_supp_addr', '', '', doc, cdt, cdn, 1);

}

cur_frm.fields_dict['production_order'].get_query = function(doc) {
	return{
		filters:[
			['Production Order', 'docstatus', '=', 1],
			['Production Order', 'qty', '>','`tabProduction Order`.produced_qty']
		]
	}
}

cur_frm.cscript.purpose = function(doc, cdt, cdn) {
	cur_frm.cscript.toggle_related_fields(doc);
}

// Overloaded query for link batch_no
cur_frm.fields_dict['mtn_details'].grid.get_field('batch_no').get_query = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];		
	if(d.item_code) {
		return{
			query: "stock.doctype.stock_entry.stock_entry.get_batch_no",
			filters:{
				'item_code': d.item_code,
				's_warehouse': d.s_warehouse,
				'posting_date': doc.posting_date
			}
		}			
	} else {
		msgprint(wn._("Please enter Item Code to get batch no"));
	}
}

cur_frm.cscript.item_code = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	args = {
		'item_code'			: d.item_code,
		'warehouse'			: cstr(d.s_warehouse) || cstr(d.t_warehouse),
		'transfer_qty'		: d.transfer_qty,
		'serial_no'			: d.serial_no,
		'bom_no'			: d.bom_no,
		'expense_account'	: d.expense_account,
		'cost_center'		: d.cost_center,
		'company'			: cur_frm.doc.company
	};
	return get_server_fields('get_item_details', JSON.stringify(args), 
		'mtn_details', doc, cdt, cdn, 1);
}

cur_frm.cscript.s_warehouse = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	args = {
		'item_code'		: d.item_code,
		'warehouse'		: cstr(d.s_warehouse) || cstr(d.t_warehouse),
		'transfer_qty'	: d.transfer_qty,
		'serial_no'		: d.serial_no,
		'bom_no'		: d.bom_no,
		'qty'			: d.s_warehouse ? -1* d.qty : d.qty
	}
	return get_server_fields('get_warehouse_details', JSON.stringify(args), 
		'mtn_details', doc, cdt, cdn, 1);
}

cur_frm.cscript.t_warehouse = cur_frm.cscript.s_warehouse;

cur_frm.cscript.uom = function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	if(d.uom && d.item_code){
		var arg = {'item_code':d.item_code, 'uom':d.uom, 'qty':d.qty}
		return get_server_fields('get_uom_details', JSON.stringify(arg), 
			'mtn_details', doc, cdt, cdn, 1);
	}
}

cur_frm.cscript.validate = function(doc, cdt, cdn) {
	cur_frm.cscript.validate_items(doc);
	if($.inArray(cur_frm.doc.purpose, ["Purchase Return", "Sales Return"])!==-1)
		validated = cur_frm.cscript.get_doctype_docname() ? true : false;
}

cur_frm.cscript.validate_items = function(doc) {
	cl = getchildren('Stock Entry Detail', doc.name, 'mtn_details');
	if (!cl.length) {
		alert(wn._("Item table can not be blank"));
		validated = false;
	}
}

cur_frm.cscript.expense_account = function(doc, cdt, cdn) {
	cur_frm.cscript.copy_account_in_all_row(doc, cdt, cdn, "expense_account");
}

cur_frm.cscript.cost_center = function(doc, cdt, cdn) {
	cur_frm.cscript.copy_account_in_all_row(doc, cdt, cdn, "cost_center");
}

cur_frm.fields_dict.customer.get_query = function(doc, cdt, cdn) {
	return{ query:"controllers.queries.customer_query" }
}

cur_frm.fields_dict.supplier.get_query = function(doc, cdt, cdn) {
	return{	query:"controllers.queries.supplier_query" }
}

// cur_frm.cscript.client_company = function(doc, cdt, cdn) {
// 	if(doc.client_company){
    
// 	 	return get_server_fields('get_company_address','',doc.client_company, doc, cdt, cdn, 1);
	 	
//  	}
// }

cur_frm.cscript.internal_purpose= function(doc,cdt,cdn){
	//doc.purpose='Material Transfer';
	if(doc.internal_purpose=='Inward'){

		doc.naming_series='TRU/IN';
		refresh_field('naming_series');
	}
	else{
		doc.naming_series='TRU/OUT';
		refresh_field('naming_series');
	}

	// refresh_field('purpose');
	// refresh_field('mtn_details');

}




cur_frm.get_field("electronically_approved_by_1").get_query=function(doc,cdt,cdn)
{
   return "select name from `tabProfile` where name!='"+doc.electronically_approved_by_2+"'"
}


cur_frm.get_field("electronically_approved_by_2").get_query=function(doc,cdt,cdn)
{
   return "select name from `tabProfile` where name!='"+doc.electronically_approved_by_1+"'"
}

cur_frm.get_field("outward_challan_no").get_query=function(doc,cdt,cdn){
	return "select name from `tabStock Entry` where internal_purpose='Outward' and (docstatus = 1 or docstatus=0)"
}

cur_frm.cscript.outward_challan_no=function(doc,cdt,cdn){
	get_server_fields('get_outward_details','','',doc,cdt,cdn,1,function(doc,cdt,cdn){
		refresh_field(['mtn_details','purpose']);
		cur_frm.cscript.toggle_related_fields(doc,cdt,cdn)
	})
}