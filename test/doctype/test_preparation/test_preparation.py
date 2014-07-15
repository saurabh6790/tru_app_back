# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.model.bean import getlist
from webnotes.model.doc import addchild, Document
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate
import webnotes

class DocType:

	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		self.doc.test_preparation=self.doc.name
		self.doc.save()
	def on_submit(self):
		samples = {}
		for sample in getlist(self.doclist, 'sample_details'):
			#samples[sample.get('sample_no')] = ''
			self.test_allocation(sample)
		
	def test_allocation(self,sample):
		#webnotes.errprint("in test all")
		test_id ,test_name= self.create_test(sample)
 		self.create_todo(sample,test_id,test_name)
		
	def add_equipment(self,equipment):
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	def create_test(self,sample):

		if self.doc.test=='Sediment':
			test_name='Test Of Extract'
		elif self.doc.test=='Furan Content':
			test_name = 'Furan Content'
		elif self.doc.test=='Corrossive Sulphur':
			test_name ='Corrossive Sulphur'
		# elif self.doc.test=='Accelerated Ageing':
		# 	test_name='Accelerated Ageing'
		# elif self.doc.test=='Oxidation Stability':
		# 	test_name='Oxidation Stability'
		test=Document(test_name)
		test.sample_no=sample.sample_no
		test.tested_by=sample.tester
		test.save()
		return test.name,test_name

	def create_todo(self,sample,test_id,test_name):
		userid = webnotes.conn.sql("select user_id  from tabEmployee where name = '%s'"%(sample.tester),as_list=1)
		#webnotes.errprint(userid[0][0])
		if userid:
			d = Document("ToDo")
			d.owner = userid[0][0]
			d.reference_type =test_name
			d.reference_name = test_id
			d.priority =  'Medium'
			d.date = nowdate()
			d.assigned_by = webnotes.user.name
			d.save(1)
			


# @webnotes.whitelist()
# def calculate_testing_of_extract(source_name,target_doclist=None):
# 	#webnotes.errprint(source_name)
# 	return _calculate_testing_of_extract(source_name, target_doclist)



# def _calculate_testing_of_extract(source_name, target_doclist=None, ignore_permissions=False):
# 	from webnotes.model.mapper import get_mapped_doclist


# 	doclist = get_mapped_doclist("Test Preparation", source_name, {
# 			"Test Preparation": {
# 				"doctype": "Test Of Extract", 
								
# 				"validation": {
# 					"docstatus": ["=", 1]
# 				}
# 			}
# 	},target_doclist)

# 	return [d.fields for d in doclist]




# @webnotes.whitelist()
# def calculate_furan_content(source_name, target_doclist=None):
# 	#webnotes.errprint(source_name)
# 	return _calculate_furan_content(source_name, target_doclist)

# def _calculate_furan_content(source_name, target_doclist=None, ignore_permissions=False):
# 	from webnotes.model.mapper import get_mapped_doclist


# 	doclist = get_mapped_doclist("Test Preparation", source_name, {
# 			"Test Preparation": {
# 				"doctype": "Furan Content", 
								
# 				"validation": {
# 					"docstatus": ["=", 1]
# 				}
# 			}
# 	},target_doclist)

# 	return [d.fields for d in doclist]


# @webnotes.whitelist()
# def calculate_oxidation_stability(source_name, target_doclist=None):
# 	#webnotes.errprint(source_name)
# 	return _calculate_oxidation_stability(source_name, target_doclist)

# def _calculate_oxidation_stability(source_name, target_doclist=None, ignore_permissions=False):
# 	from webnotes.model.mapper import get_mapped_doclist


# 	doclist = get_mapped_doclist("Test Preparation", source_name, {
# 			"Test Preparation": {
# 				"doctype": "Oxidation Stability", 
								
# 				"validation": {
# 					"docstatus": ["=", 1]
# 				}
# 			}
# 	},target_doclist)

# 	return [d.fields for d in doclist]


# @webnotes.whitelist()
# def calculate_corrosive_sulphur(source_name, target_doclist=None):
# 	#webnotes.errprint(source_name)
# 	return _calculate_corrosive_sulphur(source_name, target_doclist)

# def _calculate_corrosive_sulphur(source_name, target_doclist=None, ignore_permissions=False):
# 	from webnotes.model.mapper import get_mapped_doclist


# 	doclist = get_mapped_doclist("Test Preparation", source_name, {
# 			"Test Preparation": {
# 				"doctype": "Corrossive Sulphur", 
								
# 				"validation": {
# 					"docstatus": ["=", 1]
# 				}
# 			}
# 	},target_doclist)

# 	return [d.fields for d in doclist]


# @webnotes.whitelist()
# def calculate_neutralization_value(source_name, target_doclist=None):
# 	#webnotes.errprint(source_name)
# 	return _calculate_neutralization_value(source_name, target_doclist)

# def _calculate_neutralization_value(source_name, target_doclist=None, ignore_permissions=False):
# 	from webnotes.model.mapper import get_mapped_doclist
	
# 	doclist = get_mapped_doclist("Test Preparation", source_name, {
# 			"Test Preparation": {
# 				"doctype": "Neutralization Value", 
				
								
# 				"validation": {
# 					"docstatus": ["=", 1]
# 				}
# 			}
# 	},target_doclist)

# 	return [d.fields for d in doclist]



# @webnotes.whitelist()
# def prepare_sample_for_sediment(source_name, target_doclist=None):
# 	#webnotes.errprint(source_name)
# 	return _prepare_sample_for_sediment(source_name, target_doclist)

# def _prepare_sample_for_sediment(source_name, target_doclist=None, ignore_permissions=False):
# 	from webnotes.model.mapper import get_mapped_doclist
# 	#webnotes.errprint(source_name)
# 	def postprocess(source, doclist):
#  		doclist[0].test = 'Sediment'
#  		#webnotes.errprint(source)

# 	doclist = get_mapped_doclist("Test Preparation", source_name, {
# 			"Test Preparation": {
# 				"doctype": "Test Preparation", 
# 				# "field_map":{
# 				# 	"test":'Sediment'
# 				# },	
# 				"validation": {
# 					"docstatus": ["=", 1]
# 				}
# 			}
# 	},target_doclist, postprocess)

# 	return [d.fields for d in doclist]


# @webnotes.whitelist()
# def calculate_ressistivity_and_dissipiation(source_name, target_doclist=None):
# 	#webnotes.errprint(source_name)
# 	return _calculate_ressistivity_and_dissipiation(source_name, target_doclist)

# def _calculate_ressistivity_and_dissipiation(source_name, target_doclist=None, ignore_permissions=False):
# 	from webnotes.model.mapper import get_mapped_doclist
# 	#webnotes.errprint(source_name)
# 	# def postprocess(source, doclist):
#  # 		doclist[0].test = 'Sediment'
#  		#webnotes.errprint(source)

# 	doclist = get_mapped_doclist("Test Preparation", source_name, {
# 			"Test Preparation": {
# 				"doctype": "Resistivity and Dissipation", 
# 				# "field_map":{
# 				# 	"test":'Sediment'
# 				# },	
# 				"validation": {
# 					"docstatus": ["=", 1]
# 				}
# 			}
# 	},target_doclist)#postprocess)

# 	return [d.fields for d in doclist]