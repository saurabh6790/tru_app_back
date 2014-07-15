# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import get, Document


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
		
	def generate_sample_entry(self):
		#count=count+1
		se_details = eval(str(self.doc))
		se_details['doctype'] = 'Sample Entry'
		se_details['docstatus'] = '1'
		webnotes.bean(se_details).insert()
		webnotes.msgprint("Sample Entry created successfully.. Now Next step is Sample Creation!!!")
		#webnotes.errprint(count)

	def add_bottle_no(self,bottle):
		if self.doc.bottle_list:
			bottle_list = self.doc.bottle_list + ', ' + bottle
		else:
			bottle_list = bottle 
		return{	
		"bottle_list": bottle_list
		}


def get_functional_location(doctype, txt, searchfield, start, page_len, filters):
	#webnotes.errprint([filters])
	return 	webnotes.conn.sql("""select functional_location from `tabTransformer` 
			where client_name=(select delivery_to from `tabStock Entry` 
				where name=(select outward_challan_no from `tabStock Entry` 
					where name='%s'))""" %filters['inward_stock_entry'],debug=1)