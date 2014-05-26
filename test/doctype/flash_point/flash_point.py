# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from test.doctype import assign_notify
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit
from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		self.assign_flash_point_test();
		self.update_status();

	def update_status(self):
		webnotes.conn.sql("update `tabSample Allocation Detail` set status='"+self.doc.workflow_state+"' where test_id='"+self.doc.name+"' ")
		webnotes.conn.commit()
	
	def get_barcode(self,sample_no):
		self.doc.bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
		return {'bottle_no':self.doc.bottle_no}

	def assign_flash_point_test(self):
		test_details = {'test': "Flash Point", 'name': self.doc.name}
		#webnotes.errprint(test_details)
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
		test_detail = {'test': "Flash Point", 'sample_no':self.doc.sample_no,'name': self.doc.name,'method':self.doc.method, 'pgcil_limit':pgcil_limit}
		#temp,density=self.get_density_temp()}
		#self.doc.reported={'Reported value of Flash Point':self.doc.reported}
		parent=create_test_results(test_detail)
		create_child_testresult(parent,self.doc.reported,test_detail,'Flash Point')











	