# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from test.doctype import assign_notify
from test.doctype import create_test_results



class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		self.assign_density_visual_test();
		self.update_status();

	def update_status(self):
		webnotes.conn.sql("update `tabSample Allocation Detail` set status='"+self.doc.workflow_state+"' where test_id='"+self.doc.name+"' ")
		webnotes.conn.commit()
	def check_break_details(self):
		webnotes.conn.commit()


	def assign_density_visual_test(self):

		test_details = {'test': "Density And Visual Examination", 'name': self.doc.name}
		
		# for assigening ticket to the person of role Shift Incharge in worflow Shift Incharge- Lab Incharge
		if self.doc.workflow_state=='Waiting For Approval':
			test_details['incharge'] = self.doc.shift_incharge_approval
			assign_notify(test_details)

		# for assigening ticket to the person of role Lab Incharge in worflow Shift Incharge- Lab Incharge
		if self.doc.workflow_state=='Waiting For Approval Of  Lab Incharge':
			test_details['incharge'] = self.doc.lab_incharge_approval
			assign_notify(test_details)

		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			test_details={'workflow_state':self.doc.workflow_state,'sample_no':self.doc.sample_no}
			assign_notify(test_details)

	def on_submit(self):

		test_detail = {'test': "Density And Visual Examination", 'sample_no':self.doc.sample_no, 'name': self.doc.name}
		create_test_results(test_detail)
