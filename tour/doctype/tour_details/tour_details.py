# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def get_address(self,client):
		#webnotes.errprint(client)
		address=webnotes.conn.sql("select concat(address_line1,'\n',city,'\n',country,'\n',phone) from `tabAddress` where customer='"+client+"'",debug=1)
		#webnotes.errprint(address[0][0])
		if address:

			return{
				'address':address[0][0]
			}
		else:
			webnotes.msgprint("There is no any address recorded for client='"+client+"'")

	def get_contactno(self,contact):
		#webnotes.errprint(conatct)
		contactno=webnotes.conn.sql("select mobile_no from `tabContact` where name='"+contact+"'",debug=1)
		webnotes.errprint(contactno)
		if contactno:

			return{
				'contact_no':contactno[0][0]
			}
		else:
			webnotes.msgprint("No any mobile number is recorded against current contact='"+contact+"'")


@webnotes.whitelist()
def create_report(source_name, target_doclist=None):
	from webnotes.model.mapper import get_mapped_doclist

	doclist = get_mapped_doclist("Tour Details", source_name, 
		{"Tour Details": {
			"doctype": "Tour Report",
			"field_map": {
				"from_date": "from_date",
				"to_date": "to_date"
				},
			"validation": {
				"docstatus": ["=", 1]
			}

			},
			"Tour Client Details": {
			"doctype": "Tour Daily Report", 
			"field_map": {
				"client_name": "client_name",
				"contact_person":"contact_person" 
				
			},
			"add_if_empty": True
		}

		}, target_doclist)
		
	return [d if isinstance(d, dict) else d.fields for d in doclist]
