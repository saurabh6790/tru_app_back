# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

mapper = {"Physical Condition And Density":['name', 'color', 'smell', 'particles','final_density'], 
	"Moisture Content":['name', 'moisture'], 
	"Dissolved Gas Analysis Detail":['parent'],
	"Breakdown Voltage":['name','break_down_temperature','break_down_humidity','break_down_ir','break_down_frequency'],
	"Flash Point":['name','reported'],
	"Furan Content":['name','hydroxymythyl_furaldehyde','furfuryl_alcohol','furaldehyde','acetyl_furan','mythyl_furaldehyde'],
	"Kinematic Viscocity":['name','reported_viscosity'],
	"Pour Point":['name','temperature_ir'],
	"PCB":['name','reported_in_ppm_0','reported_in_ppm_1','reported_in_ppm_2','reported_in_ppm_others'],
	"Corrossive Sulphur":['name','visual_observation'],
	"Oxidation Inhibiters":['name','phenol_type_inhibiter','amine_type','di_infrared_spectrophotometry','dpc'],
	"Metal In Oil":['name','aluminium','copper','iron','lead','silver','tin','zinc'],
	"Interfacial Tension":['name','ift'],
	"Test Of Extract":['name','diffrence'],
	"Resistivity and Dissipation": {'Resistivity and Dissipation':['name', 'sigma_value'], 
		'Tan Alpha Details': ['parent','tan_value'], "Resistivity Details":['parent','resistivity_value']},
	"Neutralization Value": {"Neutralization Test Details":['parent','reported_value']}
	}

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def get_details(self):
		tests = self.get_sample_wise_test(self.doc.sample_no)
		results = self.get_test_wise_results(tests, self.doc.sample_no)
		return {"results": results}

	def get_sample_wise_test(self, sample_id):
		tests = self.check_group_or_other(sample_id)
		if tests:
			return tests

	def check_group_or_other(self, sample_id):
		test_required = webnotes.conn.sql("""select test_name from `tabRegister Test Name` 
			where parent in (select name from `tabTest Allocation` 
				where sample_no = '%s' and docstatus=1) """%(sample_id), as_list=1)
		return test_required

	def get_test_wise_results(self, tests, sample_id):
		results = {}

		for test in tests:
			if test[0] in mapper:
				if isinstance(mapper.get(test[0]), list):
					self.get_result(test[0], sample_id, results)

				elif isinstance(mapper.get(test[0]), dict):
					for sub_test in mapper.get(test[0]):
						self.get_result(sub_test, sample_id, results, mapper.get(test[0])[sub_test])

		return results

	def get_result(self,test, sample_id, results, list_val=None):

		if list_val:
			args = {'cols':', '.join(list_val), 'test': test, 'sample_id': sample_id}
		else :
			args = {'cols': ', '.join(mapper.get(test)), 'test': test, 'sample_id':sample_id}

		result = webnotes.conn.sql("""select %(cols)s from `tab%(test)s` 
			where sample_no = '%(sample_id)s' and docstatus=1"""%args, as_dict=1)
		results[test] = result
