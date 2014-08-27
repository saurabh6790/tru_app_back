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

		if self.doc.test=='Oxidation Stability':
			test_id, userid = self.get_preparation_sample()
			user = webnotes.conn.sql("select user_id  from tabEmployee where name = '%s'"%(userid),as_list=1)
			self.create_todo(user,test_id)
		elif self.doc.test=='Accelerated Aging':
			test_id, userid = self.get_preparation_sample()
			user = webnotes.conn.sql("select user_id  from tabEmployee where name = '%s'"%(userid),as_list=1)
			self.create_todo(user,test_id)	
			for sample in getlist(self.doclist, 'sample_details'):
				self.test_allocation(sample)		
		else:
			for sample in getlist(self.doclist, 'sample_details'):
				self.test_allocation(sample)

				
	def test_allocation(self,sample):
		#webnotes.errprint("in test all")
		test_id = self.create_test(sample)
		userid = webnotes.conn.sql("select user_id  from tabEmployee where name = '%s'"%(sample.tester),as_list=1)
		#webnotes.errprint(test_id)
		#webnotes.errprint(userid)
 		if userid:
 			self.create_todo(userid, test_id)
		

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
			return self.create_test_doc(sample, test_name)
		elif self.doc.test=='Furan Content':
			test_name = 'Furan Content'
			return self.create_test_doc(sample, test_name)
		elif self.doc.test=='Corrossive Sulphur':
			test_name ='Corrossive Sulphur'
			return self.create_test_doc(sample, test_name)
		elif self.doc.test=='Accelerated Aging':
			test_name='Resistivity and Dissipation'
			return self.create_test_doc(sample, test_name)
	def get_preparation_sample(self):
			#webnotes.errprint("executing get_preparation_sample")
			if self.doc.test=='Oxidation Stability':
				test_mapper = {"Oxidation Stability":
										{'Neutralization Value':{
													'child_mapper': 'Neutralization Test Details',
													'type': ''
												},
										'Test Preparation':{
													'child_mapper': 'Sample Preparation Details',
													'type': 'Sediment'
												}
									}
							}
			elif self.doc.test=='Accelerated Aging':

				test_mapper = {"Accelerated Aging":
										{'Neutralization Value':{
													'child_mapper': 'Neutralization Test Details',
													'type': ''
												},
										'Test Preparation':{
													'child_mapper': 'Sample Preparation Details',
													'type': 'Sediment'
												}
									}
							}

			samples_details = webnotes.conn.sql("""select sample_no, tester, specification 
				from `tabSample Preparation Details` 
				where parent = '%s'"""%(self.doc.name),as_list=1)

			return self.create_test_document(samples_details, test_mapper), samples_details[0][1]
					
	def create_test_document(self, samples, test_mapper):
		#webnotes.errprint("executing create_test_document")
		test_result = {}
		for test_name in test_mapper.get(self.doc.test):
			test = Document(test_name)
			
			if test_name == 'Neutralization Value':
				test.tested_by = samples[0][1] 
				test.specification=samples[0][2]
				test.save() 


			if test_name == 'Test Preparation':
				test.test = test_mapper.get(self.doc.test).get(test_name).get('type')
				test.save() 
				
			self.create_child_test_document(samples, test.name, test_name, test_mapper.get(self.doc.test).get(test_name))
			test_result[test_name] = test.name 
		#webnotes.errprint(test_result)
		return test_result

	def create_child_test_document(self, samples, parent, test_name, child_details):
		for sample in samples:
			ch = Document(child_details.get('child_mapper'))
			ch.sample_no = sample[0]
			ch.parent = parent

			if test_name == "Test Preparation":
				ch.tester = sample[1]
				ch.specification = sample[2]

			ch.save()

	def create_test_doc(self, sample, test_name):
		#webnotes.errprint("create test document")
		test=Document(test_name)
		test.sample_no=sample.sample_no
		if test_name == "Test Of Extract":
			test.total_weight_of_oil = self.doc.total_weight_of_oil
		test.tested_by=sample.tester
		test.save()
		#webnotes.errprint(test)
		return {test_name: test.name}

	def create_todo(self,userid,test_id):
		#webnotes.errprint(userid[0][0])
		for key in test_id:
			#webnotes.errprint([key, test_id[key]])
			d = Document("ToDo")
			d.owner = userid[0][0]
			d.reference_type = key
			d.reference_name = test_id[key]
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