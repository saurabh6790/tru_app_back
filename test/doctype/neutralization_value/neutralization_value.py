# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from test.doctype import assign_notify
from test.doctype import create_test_results,create_child_testresult, get_pgcil_limit
from webnotes.model.bean import getlist

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		self.assign_neutralization_value_test()
		self.update_status()

	def validate(self):
		self.check_duplicate_sample_id()
		self.check_reported_value()

	def check_duplicate_sample_id(self):
		sample_no=[]
		for d in getlist(self.doclist, 'neutralisation_test_details'):
			if d.sample_no:
				if d.sample_no in sample_no:
					webnotes.msgprint("Sample no could not be duplicate",raise_exception=1)
				sample_no.append(d.sample_no)

	def check_reported_value(self):
		for d in getlist(self.doclist, 'neutralisation_test_details'):
			if not d.reported_value:
				webnotes.msgprint("Reported value could not be blank",raise_exception=1)

	def retrieve_normality_values(self):
		self.doc.normality_of_hcl=webnotes.conn.get_value('Normality',self.doc.normality,'normality')
		self.doc.volume=webnotes.conn.get_value('Normality',self.doc.normality,'volume')
		self.doc.koh_volume=webnotes.conn.get_value('Normality',self.doc.normality,'koh_volume')
		self.doc.normality_of_koh=webnotes.conn.get_value('Normality',self.doc.normality,'koh_normality')
		self.doc.method=webnotes.conn.get_value('Normality',self.doc.normality,'method')
		return "Done"

	def update_status(self):
		webnotes.conn.sql("update `tabSample Allocation Detail` set status='"+self.doc.workflow_state+"' where test_id='"+self.doc.name+"' ")
		webnotes.conn.commit()
	
	def get_barcode(self,sample_no):
		bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
		return {'bottle_no':bottle_no}


	def assign_neutralization_value_test(self):

		test_details = {'test': "Neutralization Value", 'name': self.doc.name}
		
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
		self.create_testresult()

	def create_testresult(self):
		for g in getlist(self.doclist,'neutralisation_test_details'):
			if g.reported_value:
				pgcil_limit = get_pgcil_limit(self.doc.method)
	 			test_detail = {'test': "Neutralization Value", 'sample_no':g.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit}
	 			parent=create_test_results(test_detail)
	 			create_child_testresult(parent,g.reported_value,test_detail,'Neutralization Value (Total Acidity)')	
