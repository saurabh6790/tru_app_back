# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_submit(self):
		webnotes.conn.sql("""update `tabTender` set tender_name='%s'
	 		where name='%s'"""%(self.doc.name, self.doc.name))
		webnotes.conn.sql('commit')	




@webnotes.whitelist()
def make_quotation(source_name, target_doclist=None):
	from webnotes.model.mapper import get_mapped_doclist
		
	doclist = get_mapped_doclist("Tender", source_name, 
		{"Tender": {
			"doctype": "Quotation",
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
	#webnotes.msgprint([d if isinstance(d, dict) else d.fields for d in doclist])	
	return [d if isinstance(d, dict) else d.fields for d in doclist]