# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	
@webnotes.whitelist()
def create_new_employee(source_name, target_doclist=None):
	#name=webnotes.conn.sql("select employee_name from `tabJob Application Form` where name='"+source_name+"'")
	#webnotes.errprint(name[0])
	from webnotes.model.mapper import get_mapped_doclist
	# def set_missing_values(source, target):	
	# 	target[0].employee_name = name[0][0]
	# 	#webnotes.errprint(target[0].employee_name)
	doclist = get_mapped_doclist("Job Application Form", source_name, 
		{"Job Application Form": {
			"doctype": "Employee",
			
		}}, target_doclist)
	#webnotes.msgprint([d if isinstance(d, dict) else d.fields for d in doclist])	
	return [d if isinstance(d, dict) else d.fields for d in doclist]