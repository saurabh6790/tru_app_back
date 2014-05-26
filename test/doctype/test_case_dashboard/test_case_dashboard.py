# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
mapper = {"Physical Condition And Density":['name', 'color', 'smell', 'particles','final_density'], 
	"Moisture Content":['name', 'moisture'], "Resistivity and Dissipation": ['name', 'tan_value','sigma_value','resistivity_value'],"Breakdown Voltage":['name','break_down_temperature','break_down_humidity','break_down_ir','break_down_frequency'],"Flash Point":['name','reported'],"Neutralization Test Details":['parent','reported_value']}
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
		else:
			return webnotes.conn.sql("""select test from `tabGroup Test` 
				where parent in (select test_required from `tabSample Entry` 
					where name=(select sample_entry from tabSample where name = '%s'))"""%(sample_id),as_list=1)

	def check_group_or_other(self, sample_id):
		test_required = webnotes.conn.sql(""" select test_required, name from `tabSample Entry`
		 where name = (select sample_entry from tabSample where name = '%s')"""%(sample_id))[0][0]
		if test_required == 'Others':
			return webnotes.conn.sql(""" select test from `tabRegister Test Details` 
				where parent = '%s' """%(test_required[0][1]), as_list=1)

	def get_test_wise_results(self, tests, sample_id):
		results = {}
		for test in tests:
			if test[0]=='Neutralization Value':
				test[0]='Neutralization Test Details'				
			if test[0] in mapper:
				result = webnotes.conn.sql("select %s from `tab%s` where sample_no = '%s' and docstatus=1"%(', '.join(mapper.get(test[0])), test[0], sample_id), as_dict=1)
				results[test[0]] = result

		return results