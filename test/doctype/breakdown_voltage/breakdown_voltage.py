# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
# from test.doctype import assign_notify
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit ,verfy_bottle_number,update_test_log
from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#self.update_status();
		self.calculate_avg()
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)
		

			 	
	# def get_barcode(self,sample_no):
	# 	self.doc.bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
	# 	return {'bottle_no':self.doc.bottle_no}

	# def calcualte_voltage(self):
	# 	webnotes.errprint("in calculate voltage")
	# 	cal=cstr(self.doc.break_down_temperature*self.doc.break_down_humidity)
	# 	webnotes.errprint(cal)
	# 	cal1=cstr(self.doc.break_down_ir* self.doc.break_down_frequency)


	def calculate_avg(self):
		avg_values=webnotes.conn.sql("""select sum(a.temparature)/count(a.temparature),
			sum(a.humidity)/count(a.humidity),sum(a.frequency)/count(a.frequency),sum(a.ir)/count(a.ir)
			from `tabBreak Details` a, `tabBreakdown Voltage` b where a.parent=b.name 
			and b.name='%s' and a.final_result=1"""%(self.doc.name),as_list=1)
		self.doc.break_down_temperature=avg_values[0][0]
		self.doc.break_down_humidity=avg_values[0][1]
		self.doc.break_down_frequency=avg_values[0][2]
		self.doc.break_down_ir=avg_values[0][3]

	def add_equipment(self,equipment):
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	def validate(self):
		#webnotes.errprint(self.doc.workflow_state)
		self.check_break_details()

	def check_break_details(self):
		count=0
		for m in getlist(self.doclist, 'break_detail'):
			if m.final_result==1:
				#webnotes.errprint(m.break_no)
				count=count+1
				#webnotes.errprint(count)
		if count>=6:
			pass
		else:
			#webnotes.errprint(count)
			webnotes.msgprint("Minimum six records needed for consideration of final result from Break Details Child Table.",raise_exception=1);

	
	def on_submit(self):
		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Breakdown Voltage", 'sample_no':self.doc.sample_no,'name': self.doc.name,'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by}
		voltage={'Avg Temp of Dielectric strength of oil B.D.V. in KVolume':self.doc.break_down_temperature,'Avg humidity of Dielectric strength of oil B.D.V. in KVolume':self.doc.break_down_humidity,'Avg frequency of Dielectric strength of oil B.D.V. in KVolume':self.doc.break_down_frequency,'Avg IR of Dielectric strength of oil B.D.V. in KVolume':self.doc.break_down_ir}
		if self.doc.workflow_state=='Rejected':

			update_test_log(test_detail)

		else:

			parent=create_test_results(test_detail)
			for val in voltage:
				create_child_testresult(parent,voltage[val],test_detail,val)


