# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from test.doctype import assign_notify
from test.doctype import create_test_results
from test.doctype import create_child_testresult
from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		self.assign_interfacial_tension_test();
		self.update_status();
		self.doc.density_of_oil=self.generate_testresult()
		self.doc.save()

	def generate_testresult(self):
		if self.doc.temperature_data and self.doc.temparature:
			cal=cstr(cint(1)+(0.00065*flt((flt(self.doc.temperature_data)-flt(self.doc.temparature)))))
			return cstr(flt(self.doc.density_data)*flt(cal))

	def update_status(self):
		webnotes.conn.sql("update `tabSample Allocation Detail` set status='"+self.doc.workflow_state+"' where test_id='"+self.doc.name+"' ")
		webnotes.conn.commit()
	def check_break_details(self):
		webnotes.conn.commit()


	def assign_interfacial_tension_test(self):

		test_details = {'test': "Interfacial Tension", 'name': self.doc.name}
		
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

		test_detail = {'test': "Interfacial Tension", 'sample_no':self.doc.sample_no,'name': self.doc.name}
		create_test_results(test_detail)







