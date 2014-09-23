# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
from test.doctype import assign_notify,verfy_bottle_number,update_test_log
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#self.assign_pcb_test()
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)



	def add_equipment(self,equipment):
		#webnotes.errprint(equipment)
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}


	
	def on_submit(self):
		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Furan Content", 'sample_no':self.doc.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
		else:

			parent = create_test_results(test_detail)

			child_result = {}

			child_result['Arcolor - ' + self.doc.arcolor_0] = self.doc.reported_in_ppm_0
			child_result['Arcolor - ' + self.doc.arcolor_1] = self.doc.reported_in_ppm_1
			child_result['Arcolor - ' + self.doc.arcolor_2] = self.doc.reported_in_ppm_2
			child_result['Arcolor - ' + self.doc.others] = self.doc.reported_in_ppm_others

			for child in child_result:
				create_child_testresult(parent,child_result[child],test_detail,child)

		