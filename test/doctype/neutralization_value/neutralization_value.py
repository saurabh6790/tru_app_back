# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from test.doctype import assign_notify
from test.doctype import create_test_results,create_child_testresult, get_pgcil_limit,update_test_log
from webnotes.model.doc import addchild
from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		#Assign To Function
		webnotes.errprint("in on_update")
		#self.update_status()
		self.check_bottle_no()
		#self.calculate_neutralisation_value()
	def check_bottle_no(self):
		for d in getlist(self.doclist,'neutralisation_test_details'):
			webnotes.errprint(d.sample_no)
			if cint(webnotes.conn.sql("""select count(*) from tabSample 
				where name='%s' and barcode like '%%%s%%'"""%(d.sample_no,d.bottle_no),debug=1)[0][0]) != 1:
				webnotes.msgprint("Entered bottle number not belongs to Sample No '"+d.sample_no+"' Please correct it",raise_exception=1)
			else:
				pass


	def add_equipment(self,equipment):
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}


	def get_density_details(self,args):
		dic=eval(args)
		if ((dic['temperature_data']) and (dic['density'])):
			cal=cstr(cint(1)+(0.00065*flt((flt(dic['temperature_data'])-flt(dic['temp'])))))
			density= cstr(flt(dic['density'])*flt(cal))

			return{
			"density_of_oil":density
		}
		else:
			webnotes.msgprint("Density & Temperature Field Can not be blanked")




	def get_neutralisation_details(self,args):
		#webnotes.errprint(args)
		dic=eval(args)
		cal1=cstr(56.1*(flt(dic['alkoh'])*flt(self.doc.normality_of_koh)))
		neutralisation=cstr(flt(cal1)/(flt(dic['density'])*flt(dic['volume'])))
		return{
			"reported_value":neutralisation
		}

	def validate(self):
		self.check_duplicate_sample_id()
		self.check_reported_value()

	def check_duplicate_sample_id(self):
		sample_no=[]
		for d in getlist(self.doclist, 'neutralisation_test_details'):
			if d.sample_no:
				if d.sample_no in sample_no:
					webnotes.msgprint("Sample no could not be duplicate",raise_exception=1)
				sample_no.append(d.sample_no)

	def check_reported_value(self):
		for d in getlist(self.doclist, 'neutralisation_test_details'):
			if not d.reported_value:
				webnotes.msgprint("Reported value could not be blank",raise_exception=1)

	def retrieve_normality_values(self):
		self.doc.normality_of_hcl=webnotes.conn.get_value('Normality',self.doc.normality,'normality')
		self.doc.volume=webnotes.conn.get_value('Normality',self.doc.normality,'volume')
		self.doc.koh_volume=webnotes.conn.get_value('Normality',self.doc.normality,'koh_volume')
		self.doc.normality_of_koh=webnotes.conn.get_value('Normality',self.doc.normality,'koh_normality')
		self.doc.method=webnotes.conn.get_value('Normality',self.doc.normality,'method')
		return "Done"

	def update_status(self):
		webnotes.conn.sql("update `tabSample Allocation Detail` set status='"+self.doc.workflow_state+"' where test_id='"+self.doc.name+"' ")
		webnotes.conn.commit()
	
	def get_barcode(self,sample_no):
		bottle_no=webnotes.conn.get_value('Sample',sample_no,'barcode')
		return {'bottle_no':bottle_no}
		
	def assign_neutralization_value_test(self):

		test_details = {'test': "Neutralization Value", 'name': self.doc.name}
		
		# for assigening ticket to the person of role Shift Incharge in worflow Shift Incharge- Lab Incharge
		if self.doc.workflow_state=='Waiting For Approval':
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
		self.create_testresult()
		if self.doc.workflow_state=='Rejected':
			#webnotes.errprint(self.doc.workflow_state)
			update_test_log(test_detail)

	# def update_status(self):
	# 	if self.doc.test=='Oxidation Stability':
	# 		webnotes.conn.sql("update `tabSample Preparation Details` set status='Completed' where sample_no='"+self.doc.sample_no+"' and parent='"+self.doc.test_preparation+"'",debug=1)
	# 		webnotes.conn.sql("commit")


	def add_sample_nos(self):
		if self.doc.sample_no and self.doc.physical_condition_density:
			bottle_no= webnotes.conn.sql("select barcode from `tabSample` where name='"+self.doc.sample_no+"'",debug=1)
			webnotes.errprint(bottle_no[0][0])
			self.doclist=self.doc.clear_table(self.doclist,'neutralisation_test_details')
			nl = addchild(self.doc, 'neutralisation_test_details', 'Neutralization Test Details', self.doclist)
			nl.sample_no =self.doc.sample_no
			nl.bottle_no=bottle_no[0][0]

		# elif self.doc.test=='Accelerated Aging':
		# 	sample_details = webnotes.conn.sql("select sample_no,bottle_no from `tabSample Preparation Details` s,`tabTest Preparation` p where s.parent='"+self.doc.test_preparation+"' and p.test='Accelerated Aging' and s.parent=p.name",as_dict=1,debug=1)
		# 	self.doclist=self.doc.clear_table(self.doclist,'neutralisation_test_details')
		# 	if sample_details:
		# 		webnotes.errprint(sample_details)
		# 		for sample in sample_details:
		# 			webnotes.errprint(sample['sample_no'])
		# 			nl = addchild(self.doc, 'neutralisation_test_details', 'Neutralization Test Details', self.doclist)
		# 			nl.sample_no = sample['sample_no']
		# 			nl.bottle_no=sample['bottle_no']

		# else:
		# 	pass



		
	def create_testresult(self):
		for g in getlist(self.doclist,'neutralisation_test_details'):
			if g.reported_value:
				pgcil_limit = get_pgcil_limit(self.doc.method)
	 			test_detail = {'test': "Neutralization Value", 'sample_no':g.sample_no,'name': self.doc.name, 'method':self.doc.method, 'pgcil_limit':pgcil_limit}
	 			parent=create_test_results(test_detail)
	 			create_child_testresult(parent,g.reported_value,test_detail,'Neutralization Value (Total Acidity)')	

def get_physical_density_details(doctype, txt, searchfield, start, page_len, filters):
	#webnotes.errprint([filters])
	return 	webnotes.conn.sql("""select name from `tabPhysical Condition And Density` 
			 where sample_no='%s' and docstatus=1""" %filters['sample_no'],debug=1)

# def get_sample_details(doctype, txt, searchfield, start, page_len, filters):
# 	#webnotes.errprint([filters])
# 	return 	webnotes.conn.sql("""select s.sample_no from `tabSample Preparation Details` s,
# 		`tabTest Preparation` p where s.parent=p.name and s.parent='%s' 
# 		and p.docstatus=1 and s.status='Pending'""" %filters['test_preparation'],debug=1)
			

@webnotes.whitelist()
def prepare_sample_for_sediment(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _prepare_sample_for_sediment(source_name, target_doclist)

def _prepare_sample_for_sediment(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist
	#webnotes.errprint(source_name)
	def postprocess(source, doclist):
 		doclist[0].test = 'Sediment'
 		#webnotes.errprint(source)

	doclist = get_mapped_doclist("Neutralization Value", source_name, {
			"Neutralization Value": {
				"doctype": "Test Preparation", 
				# "field_map":{
				# 	"test":'Sediment'
				# },	
				"validation": {
					"docstatus": ["=", 1]
				}
			}
		
	},target_doclist, postprocess)

	return [d.fields for d in doclist]


	
