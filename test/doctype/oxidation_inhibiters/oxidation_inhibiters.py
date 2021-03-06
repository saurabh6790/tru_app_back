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
		#self.assign_oxidation_inhibiters_test();
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)
		self.create_result_record('Running')



	def add_equipment(self,equipment):
		#webnotes.errprint(equipment)
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	def assign_oxidation_inhibiters_test(self):
		test_details = {'test': "Oxidation Inhibiters", 'name': self.doc.name}
		
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
		self.create_result_record('Confirm')


	def create_result_record(self,status):

		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Oxidation Inhibiters", 'sample_no':self.doc.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by,'status':status}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
		else:

			parent = create_test_results(test_detail)

			child_result = {}

			child_result['Phenol Type Inhibiter'] = self.doc.phenol_type_inhibiter
			child_result['Amine Type Inhibiter ']  = self.doc.amine_type
			child_result['Di-Tert-Butyl-Paracresol By Infrared Spectrophotometry'] = self.doc.di_infrared_spectrophotometry
			child_result['DPC'] = self.doc.dpc

			for child in child_result:
				create_child_testresult(parent,child_result[child],test_detail,child)