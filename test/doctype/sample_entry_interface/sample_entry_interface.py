# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import get, Document


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl



	#to create sample entry document from sample entry interface on clicking generate sample entry button
	def generate_sample_entry(self):
		#count=count+1
		if self.doc.functional_location and self.doc.bottle_owner:

			se_details = eval(str(self.doc))
			se_details['doctype'] = 'Sample Entry'
			se_details['docstatus'] = '1'
			webnotes.bean(se_details).insert()
			webnotes.msgprint("Sample Entry created successfully.. Now Next step is Sample Creation!!!")
			#webnotes.errprint(count)
		else:
			webnotes.msgprint("Mandatory fields are required to create sample entry")

		self.update_inward_flag()


	def update_inward_flag(self):
		webnotes.conn.sql("""update `tabStock Entry` set flag1=1 
					   where name='%s'""" %(self.doc.inward_stock_entry),as_list=1)
		webnotes.conn.sql("commit")

	# add multiple bottle number
	def add_bottle_no(self,bottle):
		if self.doc.bottle_list:
			bottle_list = self.doc.bottle_list + ', ' + bottle
		else:
			bottle_list = bottle 
		return{	
		"bottle_list": bottle_list
		}


# To select if functional location is avilable or not against the customer which is involve din the inward entry which number is currently present on sample entry
def get_functional_location(doctype, txt, searchfield, start, page_len, filters):
	#webnotes.errprint([filters])
	return 	webnotes.conn.sql("""select functional_location from `tabTransformer` 
			where client_name=(select delivery_to from `tabStock Entry` 
				where name=(select outward_challan_no from `tabStock Entry` 
					where name='%s'))""" %filters['inward_stock_entry'],debug=1)



# To select if barcode involve in the inward entry which number is currently present on sample entry
def get_bottle_no(doctype, txt, searchfield, start, page_len, filters):
	#webnotes.errprint([filters])
	sample_no= webnotes.conn.sql("""select serial_no from `tabStock Entry Detail` 
			where parent='%s'""" %filters['inward_stock_entry'],as_list=1,debug=1)

	webnotes.errprint(sample_no[0][0].split('\n'))
	return [[sample] for sample in sample_no[0][0].split('\n')]
