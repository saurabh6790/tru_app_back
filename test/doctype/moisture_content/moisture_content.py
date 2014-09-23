# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
from webnotes.model.bean import getlist
from test.doctype import assign_notify
from test.doctype import create_test_results,update_test_log,verfy_bottle_number
from test.doctype import create_child_testresult, get_pgcil_limit


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		self.doc.density_mois=self.generate_testresult()
		if self.doc.instrument_reading and self.doc.volume and self.doc.density_mois:
			self.doc.moisture=self.calculate_moisture()
			self.doc.save()
			
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)


	# def get_density_details(self,temperature):

	def add_equipment(self,equipment):
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}
		
	def calculate_moisture(self):
		return cstr(flt(self.doc.instrument_reading)/(flt(self.doc.volume)*flt(self.doc.density_mois)))

	def generate_testresult(self):
		if self.doc.temperature_data and self.doc.temperature:
			cal=cstr(cint(1)+(0.00065*flt((flt(self.doc.temperature_data)-flt(self.doc.temperature)))))
			return cstr(flt(self.doc.density_data)*flt(cal))

	def on_submit(self):
		# if self.doc.test_type == 'Regular':
		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Moisture Content", 'sample_no':self.doc.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by}
		if self.doc.workflow_state=='Rejected':
			update_test_log(test_detail)
		else:

			parent=create_test_results(test_detail)
			if parent and self.doc.moisture: 
				create_child_testresult(parent,self.doc.moisture,test_detail,'Water Content By KARL FISCHER METHOD')

		



	def get_physical_density_details(self,sample_no):
	#webnotes.errprint([filters])
		physical_density=webnotes.conn.sql("""select name from `tabPhysical Condition And Density` 
			 	where sample_no='%s' and docstatus=1""" %(sample_no),debug=1)
		webnotes.errprint(physical_density)
		if physical_density:
			pass
		else:
			webnotes.msgprint("There is no any physical condition and density test completed against given sample no='"+sample_no+"' for moisture Content test physical condition and density is needed",raise_exception=1)

def get_physical_density_details(doctype, txt, searchfield, start, page_len, filters):
	#webnotes.errprint([filters])
	return 	webnotes.conn.sql("""select name from `tabPhysical Condition And Density` 
			 where sample_no='%s' """ %filters['sample_no'],debug=1)
	

