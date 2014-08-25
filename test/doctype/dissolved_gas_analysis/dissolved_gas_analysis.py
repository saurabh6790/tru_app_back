# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.model.doc import addchild
from webnotes.model.bean import getlist
from test.doctype import assign_notify,verfy_bottle_number,update_test_log
from test.doctype import create_test_results,create_child_testresult, get_pgcil_limit
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		#self.assign_dissolvedgas_test();
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)


	def add_equipment(self,equipment):
		#webnotes.errprint(equipment)
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}



	def get_dissolvedgas_details(self,run1):
		#webnotes.errprint(run1)
		if run1 and self.doc.run:

			reported=cstr(flt(run1)*flt(self.doc.run)*100)
			#webnotes.errprint(reported)
			return{
				"reported":reported
			}
		else:
			webnotes.msgprint("Specify Run1 For TGS")
	# def assign_dissolvedgas_test(self):
	# 	test_details = {'test': "Dissolved Gas Analysis", 'name': self.doc.name}
		
	# 	# for assigening ticket to the person of role Shift Incharge in worflow Shift Incharge- Lab Incharge
	# 	if self.doc.workflow_state=='Waiting For Approval':
	# 		test_details['incharge'] = self.doc.shift_incharge_approval
	# 		assign_notify(test_details)

	# 	# for assigening ticket to the person of role Lab Incharge in worflow Shift Incharge- Lab Incharge
	# 	if self.doc.workflow_state=='Waiting For Approval Of  Lab Incharge':
	# 		test_details['incharge'] = self.doc.lab_incharge_approval
	# 		assign_notify(test_details)

	# 	if self.doc.workflow_state=='Rejected':
	# 		test_details={'workflow_state':self.doc.workflow_state,'sample_no':self.doc.sample_no}
	# 		assign_notify(test_details)


	def fetch_gases(self):
		gases = webnotes.conn.sql("select name from tabGas where name!='TGC'")
		self.doclist=self.doc.clear_table(self.doclist,'dissolved_gas_detail')
		if gases:

			nl = addchild(self.doc, 'dissolved_gas_detail', 'Dissolved Gas Analysis Detail', self.doclist)
			nl.gas='TGC'
			for gas in gases:
				nl = addchild(self.doc, 'dissolved_gas_detail', 'Dissolved Gas Analysis Detail', self.doclist)
				nl.gas = gas
		else:
			webnotes.msgprint("There is no any Gas Recorded In Gas Table")



	def on_submit(self):
		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Dissolved Gas Analysis", 'sample_no':self.doc.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
		else:

			parent = create_test_results(test_detail)

			for gas_detail in getlist(self.doclist, 'dissolved_gas_detail'):
				if gas_detail.gas == 'TGS':
					create_child_testresult(parent,gas_detail.run1,test_detail,gas_detail.gas)					
				else:
					create_child_testresult(parent,gas_detail.reported,test_detail,gas_detail.gas)


		