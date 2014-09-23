# # Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# # MIT License. See license.txt

# # For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.utils import getdate, validate_email_add
from webnotes import msgprint, _
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def validate(self):
		self.validate_email()
		sef.validate_age()
		#self.validate_panno()



	def validate_email(self):
		if self.doc.email and not validate_email_add(self.doc.email):
			msgprint("Please enter valid Job Applicant Email")
			raise Exception
		if self.doc.email_id and not validate_email_add(self.doc.email_id):
			msgprint("Please enter valid Contact Person Email ID")
			raise Exception
		if self.doc.email_address and not validate_email_add(self.doc.email_address):
			msgprint("Please enter valid Recommendation Of Authority Email Address")
			raise Exception

	def validate_age(self):
		if self.doc.age<16:
			webnotes.msgprint("Applicant ang must be greater than 16 years")


	def validate_panno(self):
		if (self.doc.pan_no.isalpha() or self.doc.pan_no.isdigit()):  
			pass
		elif (self.doc.pan_no.isalpha() and self.doc.pan_no.isdigit()):
			pass

		else:
			webnotes.msgprint("Pan card Number follows only digits & characters")


@webnotes.whitelist()
def create_new_employee(source_name, target_doclist=None):
	from webnotes.model.mapper import get_mapped_doclist
	doclist = get_mapped_doclist("Job Application Form", source_name, 
		{"Job Application Form": {
			"doctype": "Employee",
			
		}}, target_doclist)
	return [d if isinstance(d, dict) else d.fields for d in doclist]