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

	def get_opening_date(self):
		from datetime import datetime
		webnotes.errprint(self.doc.opening_date)
		a = datetime.strptime(self.doc.opening_date, "%y-%m-%d")
		webnotes.errprint(a)
		# b = datetime.strptime(self.doc.submission_date, "%yy-%mm-%dd")
		# if a<b:
		# 	webnotes.errprint(a)
		# else:
		# 	webnotes.errprint(b)

	def validate(self):
		self.validate_estimatedcost()



	def validate_estimatedcost(self):
		if self.doc.estimated_cost:
			if self.doc.estimated_cost<=0:
				webnotes.msgprint("Estimated cost of tender must be greater than zero",raise_exception=1)




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