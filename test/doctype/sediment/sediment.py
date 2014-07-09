# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
# from test.doctype import assign_notifys
# from test.doctype import create_test_results
# from test.doctype import create_child_testresult,get_pgcil_limit
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def get_barcode(self,sample_no):
		self.doc.bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
		return {'bottle_no':self.doc.bottle_no}


	
	def add_equipment(self,equipment):
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	def on_submit(self):
		#if doc.workflow_state=='Approved By Lab Incharge':
		webnotes.msgprint("Please Do Testing Of Extract after successfully completion of Preparation Of Oil(Sediment) Test")
		



@webnotes.whitelist()
def calculate_testing_of_extract(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _calculate_testing_of_extract(source_name, target_doclist)



def _calculate_testing_of_extract(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist


	doclist = get_mapped_doclist("Sediment", source_name, {
			"Sediment": {
				"doctype": "Test Of Extract", 
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist)

	return [d.fields for d in doclist]
