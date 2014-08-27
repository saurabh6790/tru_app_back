# # Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# # MIT License. See license.txt

# # For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

@webnotes.whitelist()
def create_new_employee(source_name, target_doclist=None):
	from webnotes.model.mapper import get_mapped_doclist
	doclist = get_mapped_doclist("Job Application Form", source_name, 
		{"Job Application Form": {
			"doctype": "Employee",
			
		}}, target_doclist)
	return [d if isinstance(d, dict) else d.fields for d in doclist]