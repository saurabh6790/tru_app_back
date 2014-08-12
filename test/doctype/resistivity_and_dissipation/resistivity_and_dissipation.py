# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
from webnotes.model.bean import getlist
from test.doctype import assign_notify,verfy_bottle_number,update_test_log
from test.doctype import create_test_results
from test.doctype import create_child_testresult, get_pgcil_limit
import math
from math import exp, expm1

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	# def get_barcode(self,sample_no):
	# 	self.doc.bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
	# 	return {'bottle_no':self.doc.bottle_no}

	def on_submit(self):
		# if self.doc.test_type == 'Regular':
		#webnotes.errprint("test sssssss")
		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Resistivity and Dissipation", 'sample_no':self.doc.sample_no,'name': self.doc.name,'temperature':self.doc.temperature, 'method': self.doc.method, 'pgcil_limit': pgcil_limit}
		parent=create_test_results(test_detail)

		# values={'Dielectric Dissipation Factor':self.doc.tan_value,'Dielectric Constant Of Oil':self.doc.sigma_value,'Specific Resistivity':self.doc.resistivity_value}
		values = self.genereate_resuslt_dict()
		if parent:
			for val in values:
				create_child_testresult(parent,values[val],test_detail,val)	

		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)




	def on_update(self):
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)

		# self.calculate_tan()
		# self.calculate_sigma()
		# self.calculate_resistivity()
		# self.doc.save()

	def add_equipment(self,equipment):
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	def calculate_tan(self):
		if self.doc.power_tan:
			self.doc.tan_value=cstr('{0:.10f}'.format(math.pow(10,flt(self.doc.power_tan))))

	def calculate_sigma(self):
		if self.doc.switch and self.doc.ir:
			self.doc.sigma_value=cstr(2+((flt(self.doc.ir))/1000))
			#webnotes.errprint(self.doc.sigma_value)

	def calculate_resistivity(self):
		if self.doc.power_resistivity:
			resistivity_value='{0:.10f}'.format(flt(math.pow(10,12))*flt(math.pow(10,flt(self.doc.power_resistivity))))
			self.doc.resistivity_value=cstr(resistivity_value)
			#,'.3f' for frmating floating point
		# else:
		# 	resistivity 
	def genereate_resuslt_dict(self):
		values = {}
		cilent_temp = self.doc.temperature
		dielectric_dissipation_factor = self.get_client_specified_temp_result(cilent_temp,'tan_details', values)
		specific_resistivity = self.get_client_specified_temp_result(cilent_temp, 'resistivity_details', values)
		values = {'Dielectric Constant Of Oil':self.doc.sigma_value, 'Dielectric Dissipation Factor': dielectric_dissipation_factor, 'Specific Resistivity': specific_resistivity}
		return values

	def get_client_specified_temp_result(self, cilent_temp, field_name, values):
		for d in getlist(self.doclist, field_name):
			if field_name == 'tan_details':
				if d.test_temperature == cilent_temp:
					return d.tan_value

			if field_name == 'resistivity_details':
				if d.temperature == cilent_temp:
					return d.resistivity_value


@webnotes.whitelist()
def calculate_neutralization_value(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _calculate_neutralization_value(source_name, target_doclist)



def _calculate_neutralization_value(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist


	doclist = get_mapped_doclist("Resistivity and Dissipation", source_name, {
			"Resistivity and Dissipation": {
				"doctype": "Neutralization Value", 
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist)

	return [d.fields for d in doclist]


def get_sample_no(doctype, txt, searchfield, start, page_len, filters):
	webnotes.errprint([filters])
	return 	webnotes.conn.sql("""select sample_no from `tabSample Preparation Details` 
			 where parent='%s' and docstatus=1 """ %filters['test_preparation'],debug=1)