# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


# For Mapping Material Inward doctype to Material Transfer(Stock Entry)
@webnotes.whitelist()
def make_material_transfer(source_name, target_doclist=None):
	#webnotes.errprint("in outward")
	return _make_material_transfer(source_name, target_doclist)


def _make_material_transfer(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist
	
	# For Field Mapping From Previous doctype to next doctype
	def postprocess(source, doclist):
		doclist[0].purpose = "Material Transfer"
		doclist[0].material_inward=source_name
		doclist[0].from_warehouse='Finished Goods - TF'
		doclist[0].to_warehouse='Work In Progress - TF'
		
		
	doclist = get_mapped_doclist("Material Inward", source_name, {
			"Material Inward": {
				"doctype": "Stock Entry", 
				
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist, postprocess)

	return [d.fields for d in doclist]