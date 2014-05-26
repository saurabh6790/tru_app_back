# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.model.doc import addchild
from test.doctype import assign_notify
from test.doctype import create_test_results
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		self.assign_flash_point_test();

	def assign_flash_point_test(self):
		test_details = {'test': "Dissolved Gas Analysis", 'name': self.doc.name}
		
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


	def fetch_gases(self):
		gases = webnotes.conn.sql("select name from tabGas")
		self.doclist=self.doc.clear_table(self.doclist,'dissolved_gas_detail')
		for gas in gases:
			nl = addchild(self.doc, 'dissolved_gas_detail', 'Dissolved Gas Analysis Detail', self.doclist)
			nl.gas = gas



	def on_submit(self):

		test_detail = {'test': "Dissolved Gas Analysis", 'sample_no':self.doc.sample_no,'name': self.doc.name}
		create_test_results(test_detail)


