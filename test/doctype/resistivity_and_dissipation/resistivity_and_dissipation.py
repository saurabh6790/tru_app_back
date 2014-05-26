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
import math
from math import exp, expm1

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def get_barcode(self,sample_no):
		self.doc.bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
		return {'bottle_no':self.doc.bottle_no}

	def on_submit(self):
		if self.doc.test_type == 'Regular':
			pgcil_limit = get_pgcil_limit(self.doc.method)
			test_detail = {'test': "Resistivity and Dissipation", 'sample_no':self.doc.sample_no,'name': self.doc.name,'temperature':self.doc.test_temperature, 'method': self.doc.method, 'pgcil_limit': pgcil_limit}
			parent=create_test_results(test_detail)
			values={'Dielectric Dissipation Factor':self.doc.tan_value,'Dielectric Constant':self.doc.sigma_value,'Specific Resistivity':self.doc.resistivity_value}
			if parent:
				for val in values:
					create_child_testresult(parent,values[val],test_detail,val)				

	def on_update(self):
		self.calculate_tan()
		self.calculate_sigma()
		self.calculate_resistivity()
		self.doc.save()

	def calculate_tan(self):
		if self.doc.power_tan:
			self.doc.tan_value=cstr('{0:.10f}'.format(math.pow(10,flt(self.doc.power_tan))))

	def calculate_sigma(self):
		if self.doc.switch and self.doc.ir:
			self.doc.sigma_value=cstr(flt(self.doc.switch)/flt(self.doc.ir))

	def calculate_resistivity(self):
		if self.doc.power_resistivity:
			resistivity_value='{0:.10f}'.format(flt(math.pow(10,12))*flt(math.pow(10,flt(self.doc.power_resistivity))))
			self.doc.resistivity_value=cstr(resistivity_value)