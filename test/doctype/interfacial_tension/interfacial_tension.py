# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from test.doctype import assign_notify, verfy_bottle_number, update_test_log
from test.doctype import create_test_results
from test.doctype import create_child_testresult,get_pgcil_limit
from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
from math import sqrt


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		verfy_bottle_number(self.doc.sample_no, self.doc.bottle_no)

	def add_equipment(self,equipment):
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	def calculate_density(self):
		density = flt(self.doc.ir)/flt(self.doc.density_data)*flt(self.doc.volume)
		return {
			'density_of_oil': density
		}

	def calc_ift(self):
		
		A = (0.01452*100000*flt(self.doc.ir))/ round(flt(self.doc.circumfrence_of_ring)**2,2) * (flt(self.doc.water_density)-flt(self.doc.density_of_oil_reported_temp))
		B = 0.04534
		C = (1.679)/(flt(self.doc.radius_of_ring)/flt(self.doc.radius_of_wire))

		base_ift = A+B-C
		
		flag = False
		if base_ift < 0:
			base_ift = base_ift * -1
			flag = True

		sqrt_ = sqrt(base_ift)

		if flag:
			sqrt_ = sqrt_*(-1)

		ift_ = 0.725 + sqrt_

		ift = flt(self.doc.ir) * ift_

		return{
			'ift' : ift
		}

	def on_submit(self):
		pgcil_limit = get_pgcil_limit(self.doc.method)
		test_detail = {'test': "Interfacial Tension", 'sample_no':self.doc.sample_no,'name': self.doc.name, 'method':self.doc.method,'workflow_state':self.doc.workflow_state,'tested_by':self.doc.tested_by, 'pgcil_limit':pgcil_limit}
		if self.doc.workflow_state=='Rejected':
			update_test_log(test_detail)
		else:

			parent=create_test_results(test_detail)
			create_child_testresult(parent, self.doc.ift, test_detail, 'Interfacial tension of the oil against water @reported temp')

		
	

def get_physical_density_details(doctype, txt, searchfield, start, page_len, filters):
	#webnotes.errprint([filters])
	return 	webnotes.conn.sql("""select name from `tabPhysical Condition And Density` 
			 where sample_no='%s' and docstatus=1 """ %filters['sample_no'],debug=1)

@webnotes.whitelist()
def create_session():
	from webnotes.model.doc import Document
	d = Document('Session')
	d.status = 'Open'
	d.test_name='Interfacial Tension'
	d.save()
	return{
		'session_id':d.name
	}

@webnotes.whitelist()
def close_session(session_id):
	from webnotes.model.doc import Document
	d = Document('Session',session_id)
	d.status = 'Close'
	d.save()

	return{
		'session_id':''
	}
# @webnotes,whitelist()
# def open_session(session_id):
# 	from webnotes.model.doc import Document
# 	s= Document?('session',session_id)
# 	s.status='Open'
# 	d.save()

# 	return{
# 		'session_id':d.name
# 	}
@webnotes.whitelist()
def check_session():
	session = webnotes.conn.sql("""select name from tabSession 
		where status = 'Open' and test_name='Interfacial Tension' order by creation desc limit 1""",as_list=1)

	if session:
		return{
			'session_id':session[0][0]
		}
	else:
		return{
			'session_id':''
		}