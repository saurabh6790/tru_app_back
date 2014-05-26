# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
from webnotes.model.bean import getlist
from test.doctype import assign_notify
from test.doctype import create_test_results
from test.doctype import create_child_testresult, get_pgcil_limit


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		self.doc.density_mois=self.generate_testresult()
		if self.doc.instrument_reading and self.doc.volume and self.doc.density_mois:
			self.doc.moisture=self.calculate_moisture()
			self.doc.save()

	def calculate_moisture(self):
		return cstr(flt(self.doc.instrument_reading)/(flt(self.doc.volume)*flt(self.doc.density_mois)))

	def generate_testresult(self):
		if self.doc.temperature_data and self.doc.temperature:
			cal=cstr(cint(1)+(0.00065*flt((flt(self.doc.temperature_data)-flt(self.doc.temperature)))))
			return cstr(flt(self.doc.density_data)*flt(cal))

	def on_submit(self):
		if self.doc.test_type == 'Regular':
			pgcil_limit = get_pgcil_limit(self.doc.method)
			test_detail = {'test': "Moisture Content", 'sample_no':self.doc.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit}
			parent=create_test_results(test_detail)
			if parent and self.doc.moisture: 
				create_child_testresult(parent,self.doc.moisture,test_detail,'Water Content By KARL FISCHER METHOD')