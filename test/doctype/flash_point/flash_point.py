# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from test.doctype import assign_notify
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit, verfy_bottle_number,update_test_log
from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		#self.assign_flash_point_test();
		#self.update_status();
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

	# def update_status(self):
	# 	webnotes.conn.sql("update `tabSample Allocation Detail` set status='"+self.doc.workflow_state+"' where test_id='"+self.doc.name+"' ")
	# 	webnotes.conn.commit()
	
	# def get_barcode(self,sample_no):
	# 	self.doc.bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
	# 	return {'bottle_no':self.doc.bottle_no}

	# def assign_flash_point_test(self):
	# 	test_details = {'test': "Flash Point", 'name': self.doc.name}
	# 	#webnotes.errprint(test_details)
	# 	# for assigening ticket to the person of role Shift Incharge in worflow Shift Incharge- Lab Incharge
	# 	if self.doc.workflow_state=='Waiting For Approval':
	# 		test_details['incharge'] = self.doc.shift_incharge_approval
	# 		assign_notify(test_details)

	# 	# for assigening ticket to the person of role Lab Incharge in worflow Shift Incharge- Lab Incharge
	# 	if self.doc.workflow_state=='Waiting For Approval Of  Lab Incharge':
	# 		test_details['incharge'] = self.doc.lab_incharge_approval
	# 		assign_notify(test_details)

	# 	if self.doc.workflow_state=='Rejected':
	# 		test_details={'workflow_state':self.doc.workflow_state,'sample_no':self.doc.sample_no}
	# 		assign_notify(test_details)

	def on_submit(self):

		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Flash Point", 'sample_no':self.doc.sample_no,'name': self.doc.name,'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by}
		#temp,density=self.get_density_temp()}
		#self.doc.reported={'Reported value of Flash Point':self.doc.reported}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
		else:

			parent=create_test_results(test_detail)
			create_child_testresult(parent,self.doc.reported,test_detail,'Flash Point')

		













	