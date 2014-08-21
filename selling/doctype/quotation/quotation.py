# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cstr
from webnotes.model.bean import getlist
from webnotes.model.code import get_obj
from webnotes import _, msgprint
from webnotes.model.doc import addchild,Document
from controllers.selling_controller import SellingController
from webnotes.utils import cstr, flt, getdate
from webnotes.model.mapper import get_mapped_doclist
class DocType(SellingController):
	def __init__(self, doc, doclist=[]):
		self.doc = doc
		self.doclist = doclist
		self.tname = 'Quotation Item'
		self.fname = 'quotation_details'

	def has_sales_order(self):
		return webnotes.conn.get_value("Sales Order Item", {"prevdoc_docname": self.doc.name, "docstatus": 1})

	def validate_for_items(self):
		chk_dupl_itm = []
		for d in getlist(self.doclist,'quotation_details'):
			if [cstr(d.item_code),cstr(d.description)] in chk_dupl_itm:
				msgprint("Item %s has been entered twice. Please change description atleast to continue" % d.item_code)
				raise Exception
			else:
				chk_dupl_itm.append([cstr(d.item_code),cstr(d.description)])

	def validate_order_type(self):
		#webnotes.errprint("in the validate")
		super(DocType, self).validate_order_type()
		
		if self.doc.order_type in ['Maintenance', 'Service']:
			for d in getlist(self.doclist, 'quotation_details'):
				is_service_item = webnotes.conn.sql("select is_service_item from `tabItem` where name=%s", d.item_code)
				is_service_item = is_service_item and is_service_item[0][0] or 'No'
				
				if is_service_item == 'No':
					msgprint("You can not select non service item "+d.item_code+" in Maintenance Quotation")
					raise Exception
		else:
			for d in getlist(self.doclist, 'quotation_details'):
				is_sales_item = webnotes.conn.sql("select is_sales_item from `tabItem` where name=%s", d.item_code)
				is_sales_item = is_sales_item and is_sales_item[0][0] or 'No'
				
				if is_sales_item == 'No':
					msgprint("You can not select non sales item "+d.item_code+" in Sales Quotation")
					raise Exception
	
	def validate(self):
		super(DocType, self).validate()
		self.set_status()
		self.validate_order_type()
		#self.validate_for_items()
		self.validate_for_product()
		self.validate_uom_is_integer("stock_uom", "qty")

	def on_update(self):
		self.doc.quotation_name=self.doc.name
		self.doc.save()

		if self.doc.estimated_value and self.doc.percentage:
			amount=cstr(flt(self.doc.rounded_total_export)/flt(self.doc.percentage))
			if self.doc.estimated_value=='Percentage Above of the Estimated Cost':
				quotation_amount=flt(self.doc.rounded_total_export)+flt(amount)
				webnotes.errprint(quotation_amount)
			else:
				quotation_amount=flt(self.doc.rounded_total_export)-flt(amount)
				webnotes.errprint(quotation_amount)

			if quotation_amount:
				webnotes.errprint("in update query")
				webnotes.conn.sql("""update `tabQuotation` set quoted_amount='%s' where name='%s'"""%(quotation_amount,self.doc.name),debug=1)
				webnotes.conn.sql('commit')	
		
	def update_opportunity(self):
		for opportunity in self.doclist.get_distinct_values("prevdoc_docname"):
			webnotes.bean("Opportunity", opportunity).get_controller().set_status(update=True)
	
	def declare_order_lost(self, arg):
		if not self.has_sales_order():
			webnotes.conn.set(self.doc, 'status', 'Lost')
			webnotes.conn.set(self.doc, 'order_lost_reason', arg)
			self.update_opportunity()
		else:
			webnotes.throw(_("Cannot set as Lost as Sales Order is made."))
	
	def check_item_table(self):
		if not getlist(self.doclist, 'quotation_details'):
			msgprint("Please enter item details")
			raise Exception
		
	def on_submit(self):
		self.check_item_table()
		
		# Check for Approving Authority
		get_obj('Authorization Control').validate_approving_authority(self.doc.doctype, self.doc.company, self.doc.grand_total, self)
			
		#update enquiry status
		self.update_opportunity()
		parent=self.create_parent_sales_order()
		#webnotes.errprint(parent)

		#to create sales order from quotation
		self.create_item_sales_order(parent)
		self.create_tax_sales_order(parent)
		webnotes.conn.sql("""update `tabQuotation Item` set sales_order='%s' where parent='%s'"""%(parent,self.doc.name),debug=1)
		webnotes.conn.sql('commit')	

		webnotes.conn.sql("""update `tabQuotation Item` set quotation='%s' where parent='%s'"""%(self.doc.name,self.doc.name),debug=1)
		webnotes.conn.sql('commit')	
	def create_parent_sales_order(self):
		webnotes.errprint("in create sales order")
		d=Document('Sales Order')
		d.naming_series='PI/2011/'
		d.company=self.doc.company
		d.customer=self.doc.customer
		d.transaction_date=self.doc.transaction_date
		d.order_type=self.doc.order_type
		d.currency='INR'
		d.selling_price_list='Standard Selling'
		d.charge=self.doc.charge
		d.shipping_rule=self.doc.shipping_rule
		d.other_charges_total_export=self.doc.other_charges_total_export
		d.grand_total_export=self.doc.grand_total_export
		d.rounded_total_export=self.doc.rounded_total_export
		d.in_words_export=self.doc.in_words_export
		d.tc_name=self.doc.tc_name
		d.terms=self.doc.terms
		d.territory=self.doc.territory
		d.customer_group=self.doc.customer_group
		d.customer_address=self.doc.customer_address
		d.contact_person=self.doc.contact_person
		d.letter_head=self.doc.letter_head
		d.source=self.doc.source
		d.select_print_heading=self.doc.select_print_heading
		d.status=self.doc.status
		d.fiscal_year=self.doc.fiscal_year
		d.docstatus=1
		d.save()
		return d.name


	def create_item_sales_order(self,parent):
		webnotes.errprint("in child sales order")
		if parent:
			for i in getlist(self.doclist,'quotation_details'):
				#webnotes.errprint(i)
				ch=addchild(self.doc, 'sales_order_details', 'Sales Order Item', self.doclist)
				ch.item_code=i.item_code
				ch.item_name=i.item_name
				ch.description=i.description
				ch.test_details=i.test_details
				ch.qty=i.qty
				ch.parent=parent
				ch.parenttype='Sales Order'
				ch.parentfield='sales_order_details'
				ch.prevdoc_docname=self.doc.name
				ch.stock_uom=i.stock_uom
				ch.ref_rate=i.ref_rate
				ch.adj_rate=i.adj_rate
				ch.export_rate=i.export_rate
				ch.export_amount=i.export_amount
				ch.docstatus=1
				ch.save()
				#webnotes.errprint(ch)

	def create_tax_sales_order(self,parent):
		webnotes.errprint("in tax sales order")
		if parent:
			for j in getlist(self.doclist,'other_charges'):
				#webnotes.errprint(j)
				cd=addchild(self.doc,'other_charges','Sales Taxes and Charges',self.doclist)
				cd.charge_type=j.charge_type
				cd.row_id=j.row_id
				cd.parent=parent
				cd.parenttype='Sales Order'
				cd.parentfield='other_charges'
				cd.account_head=j.account_head
				cd.cost_center=j.cost_center
				cd.description=j.description
				cd.rate=j.rate
				cd.tax_amount=j.tax_amount
				cd.total=j.total
				cd.docstatus=1
				cd.save()
				webnotes.errprint(cd)

		
	def on_cancel(self):
		#update enquiry status
		self.set_status()
		self.update_opportunity()
			
	def print_other_charges(self,docname):
		print_lst = []
		for d in getlist(self.doclist,'other_charges'):
			lst1 = []
			lst1.append(d.description)
			lst1.append(d.total)
			print_lst.append(lst1)
		return print_lst


	def validate_for_product(self):
		chk_dupl_prd = []
		for d in getlist(self.doclist,'quotation_product'):
			if [cstr(d.product_name),cstr(d.description)] in chk_dupl_prd:
				msgprint("Product %s has been entered twice. Please change description atleast to continue" % d.product_name)
				raise Exception
			else:
				chk_dupl_prd.append([cstr(d.product_name),cstr(d.description)])	
		
	
@webnotes.whitelist()
def make_sales_order(source_name, target_doclist=None):
	return _make_sales_order(source_name, target_doclist)
	
def _make_sales_order(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist
	
	customer = _make_customer(source_name, ignore_permissions)
	
	def set_missing_values(source, target):
		if customer:
			target[0].customer = customer.doc.name
			target[0].customer_name = customer.doc.customer_name
			
		si = webnotes.bean(target)
		si.run_method("onload_post_render")
			
	doclist = get_mapped_doclist("Quotation", source_name, {
			"Quotation": {
				"doctype": "Sales Order", 
				"validation": {
					"docstatus": ["=", 1]
				}
			}, 
			"Quotation Item": {
				"doctype": "Sales Order Item", 
				"field_map": {
					"parent": "prevdoc_docname"
				}
			}, 
			# "Quotation Product": {
			# 	"doctype": "Sales Order Product", 
			# 	"field_map": {
			# 		"parent": "prevdoc_docname"
			# 	}
			# },
			"Sales Taxes and Charges": {
				"doctype": "Sales Taxes and Charges",
				"add_if_empty": True
			}, 
			"Sales Team": {
				"doctype": "Sales Team",
				"add_if_empty": True
			}
		}, target_doclist, set_missing_values, ignore_permissions=ignore_permissions)
		
	# postprocess: fetch shipping address, set missing values
		
	return [d.fields for d in doclist]

def _make_customer(source_name, ignore_permissions=False):
	quotation = webnotes.conn.get_value("Quotation", source_name, ["lead", "order_type"])
	if quotation and quotation[0]:
		lead_name = quotation[0]
		customer_name = webnotes.conn.get_value("Customer", {"lead_name": lead_name})
		if not customer_name:
			from selling.doctype.lead.lead import _make_customer
			customer_doclist = _make_customer(lead_name, ignore_permissions=ignore_permissions)
			customer = webnotes.bean(customer_doclist)
			customer.ignore_permissions = ignore_permissions
			if quotation[1] == "Shopping Cart":
				customer.doc.customer_group = webnotes.conn.get_value("Shopping Cart Settings", None,
					"default_customer_group")
			
			try:
				customer.insert()
				return customer
			except NameError, e:
				if webnotes.defaults.get_global_default('cust_master_name') == "Customer Name":
					customer.run_method("autoname")
					customer.doc.name += "-" + lead_name
					customer.insert()
					return customer
				else:
					raise
			except webnotes.MandatoryError:
				from webnotes.utils import get_url_to_form
				webnotes.throw(_("Before proceeding, please create Customer from Lead") + \
					(" - %s" % get_url_to_form("Lead", lead_name)))

@webnotes.whitelist()
def make_tender(source_name, target_doclist=None):
	from webnotes.model.mapper import get_mapped_doclist
		
	doclist = get_mapped_doclist("Quotation", source_name, 
		{"Quotation": {
			"doctype": "Tender",
			"field_map": {
				# "campaign_name": "campaign",
				# "doctype": "enquiry_from",
				# "name": "lead",
				# "lead_name": "contact_display",
				# "company_name": "customer_name",
				# "email_id": "contact_email",
				# "mobile_no": "contact_mobile"
			}
		}}, target_doclist)
		
	return [d if isinstance(d, dict) else d.fields for d in doclist]

@webnotes.whitelist()
def make_sales_invoice(source_name,target_doclist=None):
	#webnotes.errprint(args)
	def set_missing_values(source, target):
		bean = webnotes.bean(target)
		bean.doc.is_pos = 0
		bean.run_method("onload_post_render")
		
	def update_item(obj, target, source_parent):
		target.export_amount = flt(obj.export_amount) - flt(obj.billed_amt)
		target.amount = target.export_amount * flt(source_parent.conversion_rate)
		target.qty = obj.export_rate and target.export_amount / flt(obj.export_rate) or obj.qty
			
	doclist = get_mapped_doclist("Quotation", source_name, {
		"Quotation": {
			"doctype": "Sales Invoice", 
			"validation": {
				"docstatus": ["=", 1]
			}
		}, 
		"Quotation Item": {
			"doctype": "Sales Invoice Item", 
			"field_map": {
				"sales_order":"sales_order"
				#"name": "so_detail", 
			# 	"parent": "quotation",
			# 	#"reserved_warehouse": "warehouse"
			},
			# "postprocess": update_item,
			# "condition": lambda doc: doc.amount==0 or doc.billed_amt < doc.export_amount
		}, 
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges", 
			"add_if_empty": True
		}
		# "Sales Team": {
		# 	"doctype": "Sales Team", 
		# 	"add_if_empty": True
		# }
	}, target_doclist, set_missing_values)
	
	return [d.fields for d in doclist]