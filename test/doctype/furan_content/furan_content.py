# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt
from __future__ import unicode_literals
from webnotes.model.doc import addchild
from test.doctype import assign_notify
from test.doctype import create_test_results,create_child_testresult, get_pgcil_limit,verfy_bottle_number,update_test_log
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def on_update(self):
		#Assign To Function
		#self.assign_furancontent_test();
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


	def assign_furancontent_test(self):
		test_details = {'test': "Furan Content", 'name': self.doc.name}
		
		# for assigening ticket to the person of role Shift Incharge in worflow Shift Incharge- Lab Incharge
		if self.doc.workflow_state=='Waiting For Approval':
			test_details['incharge'] = self.doc.shift_incharge_approval
			assign_notify(test_details)

		# for assigening ticket to the person of role Lab Incharge in worflow Shift Incharge- Lab Incharge
		if self.doc.workflow_state=='Waiting For Approval Of  Lab Incharge':
			test_details['incharge'] = self.doc.lab_incharge_approval
			assign_notify(test_details)

		if self.doc.workflow_state=='Rejected':
			test_details={'workflow_state':self.doc.workflow_state,'sample_no':self.doc.sample_no}
			assign_notify(test_details)

	def on_submit(self):
		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Furan Content", 'sample_no':self.doc.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
		else:

			parent = create_test_results(test_detail)

			child_result = {}

			child_result['5-Hydroxymythyl 2-Furaldehyde'] = self.doc.hydroxymythyl_furaldehyde
			child_result['2-Furfuryl Alcohol'] = self.doc.furfuryl_alcohol
			child_result['2-Furaldehyde'] = self.doc.furaldehyde
			child_result['2-Acetyl Furan'] = self.doc.acetyl_furan
			child_result['5Mythyl 2-Furaldehyde'] = self.doc.mythyl_furaldehyde

			for child in child_result:
				create_child_testresult(parent,child_result[child],test_detail,child)

		
				

		
			
			