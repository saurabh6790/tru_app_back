# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		self.doc.test_preparation=self.doc.name
		self.doc.save()

	def add_equipment(self,equipment):
		if self.doc.equipment_used_list:
			equipment_list = self.doc.equipment_used_list + ', ' + equipment
		else:
			equipment_list = equipment 
		return{	
		"equipment_used_list": equipment_list
		}

	#def add_wequipment(self,args):

	# def add_equipment(self,args):
	# 	webnotes.errprint(type(args))
	# 	dic=eval(args)
	# 	webnotes.errprint(type(dic))
	# 	webnotes.errprint(dic.get('equipment_used_list'))
	# 	# if (dic.get('equipment_used_list')):
	# 	# 	equipment_list = dic.get('equipment_used_list') + ', ' + dic.get('equipment')
	# 	# else:
	# 	equipment_list = dic.get('equipment')
	# 	return{	
	# 	"equipment_used_list": equipment_list
	# 	}

@webnotes.whitelist()
def calculate_testing_of_extract(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _calculate_testing_of_extract(source_name, target_doclist)



def _calculate_testing_of_extract(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist


	doclist = get_mapped_doclist("Test Preparation", source_name, {
			"Test Preparation": {
				"doctype": "Test Of Extract", 
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist)

	return [d.fields for d in doclist]




@webnotes.whitelist()
def calculate_furan_content(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _calculate_furan_content(source_name, target_doclist)

def _calculate_furan_content(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist


	doclist = get_mapped_doclist("Test Preparation", source_name, {
			"Test Preparation": {
				"doctype": "Furan Content", 
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist)

	return [d.fields for d in doclist]


@webnotes.whitelist()
def calculate_oxidation_stability(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _calculate_oxidation_stability(source_name, target_doclist)

def _calculate_oxidation_stability(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist


	doclist = get_mapped_doclist("Test Preparation", source_name, {
			"Test Preparation": {
				"doctype": "Oxidation Stability", 
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist)

	return [d.fields for d in doclist]


@webnotes.whitelist()
def calculate_corrosive_sulphur(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _calculate_corrosive_sulphur(source_name, target_doclist)

def _calculate_corrosive_sulphur(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist


	doclist = get_mapped_doclist("Test Preparation", source_name, {
			"Test Preparation": {
				"doctype": "Corrossive Sulphur", 
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist)

	return [d.fields for d in doclist]


@webnotes.whitelist()
def calculate_neutralization_value(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _calculate_neutralization_value(source_name, target_doclist)

def _calculate_neutralization_value(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist
	
	doclist = get_mapped_doclist("Test Preparation", source_name, {
			"Test Preparation": {
				"doctype": "Neutralization Value", 
				
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist)

	return [d.fields for d in doclist]



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

	doclist = get_mapped_doclist("Test Preparation", source_name, {
			"Test Preparation": {
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


@webnotes.whitelist()
def calculate_ressistivity_and_dissipiation(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _calculate_ressistivity_and_dissipiation(source_name, target_doclist)

def _calculate_ressistivity_and_dissipiation(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist
	#webnotes.errprint(source_name)
	# def postprocess(source, doclist):
 # 		doclist[0].test = 'Sediment'
 		#webnotes.errprint(source)

	doclist = get_mapped_doclist("Test Preparation", source_name, {
			"Test Preparation": {
				"doctype": "Resistivity and Dissipation", 
				# "field_map":{
				# 	"test":'Sediment'
				# },	
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist)#postprocess)

	return [d.fields for d in doclist]