# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from test.doctype import assign_notify
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit

from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
	def on_update(self):
		#Assign To Function
		self.assign_breakdown_voltage_test();
		if self.doc.workflow_state=='Employee Call':

			self.check_break_details();
		self.update_status();
		self.calculate_avg()
		self.doc.save()

	def get_barcode(self,sample_no):
		self.doc.bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
		return {'bottle_no':self.doc.bottle_no}

	def calculate_avg(self):
		avg_values=webnotes.conn.sql("""select sum(a.temparature)/count(a.temparature),
			sum(a.humidity)/count(a.humidity),sum(a.frequency)/count(a.frequency),sum(a.ir)/count(a.ir)
			from `tabBreak Details` a, `tabBreakdown Voltage` b where a.parent=b.name 
			and b.name='%s' and a.final_result=1"""%(self.doc.name),as_list=1)
		self.doc.break_down_temperature=avg_values[0][0]
		self.doc.break_down_humidity=avg_values[0][1]
		self.doc.break_down_frequency=avg_values[0][2]
		self.doc.break_down_ir=avg_values[0][3]

	def update_status(self):
		webnotes.conn.sql("update `tabSample Allocation Detail` set status='"+self.doc.workflow_state+"' where test_id='"+self.doc.name+"' ")
		webnotes.conn.commit()
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

	def assign_breakdown_voltage_test(self):
		test_details = {'test': "Breakdown Voltage", 'name': self.doc.name}
		
		# for assigening ticket to the person of role Shift Incharge in worflow Shift Incharge- Lab Incharge
		if self.doc.workflow_state=='Waiting For Approval':
			webnotes.errprint(self.doc.workflow_state)
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

		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Breakdown Voltage", 'sample_no':self.doc.sample_no,'name': self.doc.name,'method':self.doc.method, 'pgcil_limit':pgcil_limit}
		voltage={'Avg Temp of Dielectric strength of oil B.D.V. in KVolume':self.doc.break_down_temperature,'Avg humidity of Dielectric strength of oil B.D.V. in KVolume':self.doc.break_down_humidity,'Avg frequency of Dielectric strength of oil B.D.V. in KVolume':self.doc.break_down_frequency,'Avg IR of Dielectric strength of oil B.D.V. in KVolume':self.doc.break_down_ir}
		parent=create_test_results(test_detail)
		for val in voltage:
			create_child_testresult(parent,voltage[val],test_detail,val)


