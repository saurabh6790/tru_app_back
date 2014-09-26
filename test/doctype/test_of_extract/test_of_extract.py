# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from test.doctype import assign_notify,verfy_bottle_number
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit,update_test_log
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		if self.doc.total_weight_of_oil and self.doc.weight_of_crucible and self.doc.weight_of_crucible_after:
			diff=cstr((flt(self.doc.weight_of_crucible)-flt(self.doc.weight_of_crucible_after))) #/flt(self.doc.weight_of_oil))*100
			#webnotes.errprint(diff)
			cal=cstr((flt(diff)/flt(self.doc.total_weight_of_oil))*100)
			#webnotes.errprint(cal)
			self.doc.diffrence=cal
		 	self.doc.save()

		else:
			webnotes.msgprint("All Fields must be filled")

		#self.assign_test_of_extract()
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)
		self.create_result_record('Running')




	def add_equipment(self,equipment):
		if self.doc.equipment_list:
			equipment_list = self.doc.equipment_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_list": equipment_list
		}

	def assign_test_of_extract(self):

		test_details = {'test': "Test Of Extract", 'name': self.doc.name}
		
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
		test_detail = {'test': "Test Of Extract", 'sample_no':self.doc.sample_no,'name': self.doc.name,'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by,'status':status}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
		else:

		#diffrence={'Sediment & Precipitable Sludge':self.doc.diffrence}
			parent=create_test_results(test_detail)
		#for val in voltage:
			create_child_testresult(parent,self.doc.diffrence,test_detail,'Sediment & Precipitable Sludge')

		



def get_sample_no(doctype, txt, searchfield, start, page_len, filters):
	webnotes.errprint([filters])
	return 	webnotes.conn.sql("""select sample_no from `tabSample Preparation Details` 
			 where parent='%s' and docstatus=1 """ %filters['test_preparation'],debug=1)

