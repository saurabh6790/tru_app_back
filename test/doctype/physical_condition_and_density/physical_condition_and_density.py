# # Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# # MIT License. See license.txt

# # For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
import json
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
from webnotes.model.bean import getlist
from test.doctype import assign_notify,verfy_bottle_number,update_test_log
from test.doctype import create_test_results
from test.doctype import create_child_testresult, get_pgcil_limit

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		#self.assign_physical_density_test();
		self.update_status()
		#webnotes.errprint(self.doc.temperature)
		temp,density=self.get_density_temp()
		if density:
			self.doc.density_data=density
			self.doc.temperature_data=temp
			self.doc.save()

		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)

	def validate(self):
		self.check_final_result()
	
	def add_equipment(self,equipment):
		#webnotes.errprint(equipment)
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	def update_status(self):
		webnotes.conn.sql("update `tabSample Allocation Detail` set status='"+self.doc.workflow_state+"' where test_id='"+self.doc.name+"' ")
		webnotes.conn.commit()

	
	def on_submit(self):
		# if self.doc.test_type == 'Regular':
		self.check_final_result()
		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Physical Condition And Density", 'sample_no':self.doc.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by}
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)
		else:

			temp,density=self.get_density_temp()
			parent=create_test_results(test_detail)

			if density:
				final_density=self.generate_testresult(temp,density,self.doc.temperature)
				#webnotes.errprint(final_density)
				create_child_testresult(parent,final_density,test_detail,'Density in gm/cm3')

	

	def get_density_details(self,args):
		dic=eval(args)
		sub=cstr(flt(dic['syringe'])-flt(dic['weight']))
		density=cstr(flt(sub)/flt(dic['volume']))
		return{
			"density":density
		}

	def calculate_moisture(self):
		return cstr(flt(self.doc.instrument_reading)/flt(self.doc.volume)*flt(self.doc.density_data))

	def calculate_density_for_moisture(self):
		if self.doc.temperature:
			temp,density=self.get_density_temp()
			if density:
				density_for_moisture=self.generate_testresult(temp,density,self.doc.temperature)
				return density_for_moisture

	def get_density_temp(self):
		result = None
		if self.doc.density=='By Weight':
			result=webnotes.conn.sql("select temparature,density from `tabDensity Details` where consider_for_final_result='1' and parent='%s'"%(self.doc.name),as_list=1)
		elif self.doc.density=='By Hydrometer':
			result=webnotes.conn.sql("select temparature,reported from `tabDensity Reading` where consider_for_final_result='1' and parent='%s'"%(self.doc.name),as_list=1)
		if result:
			return result[0][0],result[0][1]
		else: 
			return None, None

	def generate_testresult(self,temp,density,temp_on_job_card):
		cal1=(0.00065*flt((flt(temp)-flt(temp_on_job_card))))
		#webnotes.errprint(cal1)
		cal=cstr(cint(1)+flt(cal1))
		return cstr(flt(density)*flt(cal))

	def check_final_result(self):
		count=0
		if self.doc.density=='By Weight':

			for m in getlist(self.doclist, 'density_details'):
				if m.consider_for_final_result==1:
					#webnotes.errprint(m.break_no)
					count=count+1
					#webnotes.errprint(count)
			if count==1:
				pass
			elif count>1:
				#webnotes.errprint(count)
				webnotes.msgprint("At most one record needed for consideration of final result from Density Details Child Table.",raise_exception=1);
			elif count<1:
				webnotes.msgprint("At least one record needed for consideration of final result from Density Details Child Table.",raise_exception=1);



		if self.doc.density=='By Hydrometer':

			for n in getlist(self.doclist, 'density_reading'):
				if n.consider_for_final_result==1:
					#webnotes.errprint(m.break_no)
					count=count+1
					#webnotes.errprint(count)
			if count==1:
				pass
			elif count>1:
				#webnotes.errprint(count)
				webnotes.msgprint("At most one record needed for consideration of final result from Density Reading Child Table.",raise_exception=1);
			elif count<1:
				webnotes.msgprint("At least one record needed for consideration of final result from Density Reading Child Table.",raise_exception=1);
