# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
from test.doctype import assign_notify,verfy_bottle_number,update_test_log
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def on_update(self):
		if self.doc.viscometer_tube_constant and self.doc.time_taken:
			viscosity=cstr(flt(self.doc.viscometer_tube_constant)*(flt(self.doc.time_taken)))
			self.doc.reported_viscosity=viscosity
		 	self.doc.save()

		else:
			webnotes.msgprint("All Fields must be filled")
		
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)

	def validate(self):
		if cint(self.doc.viscometer_tube_constant) < 0 or cint(self.doc.time_taken) < 0:
			webnotes.msgprint("Viscometer Tube Constant or Time Taken should not be negative")

	def add_equipment(self,equipment):
		#webnotes.errprint(equipment)
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	


	def on_submit(self):

		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Kinematic viscosity", 'sample_no':self.doc.sample_no,'name': self.doc.name,'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by}
		#diffrence={'Sediment & Precipitable Sludge':self.doc.diffrence}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
	
		else:

			parent=create_test_results(test_detail)
			#for val in voltage:
			create_child_testresult(parent,self.doc.reported_viscosity,test_detail,'Kinematic viscosity(In Cst)')

		