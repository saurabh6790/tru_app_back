# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.bean import getlist
from webnotes.utils import cstr, flt

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl



	def on_update(self):
		self.update_test_names()

	def update_test_names(self):
		webnotes.errprint("in the update_test_names")
		test_name_list=[]
		test_name_detail=''
		for d in getlist(self.doclist,'test_details'):
			test_name_detail=d.test_name+'-'+d.test_method
			test_name_list.append(cstr(test_name_detail))
		self.doc.product_test_name='\n'.join(test_name_list)	

		webnotes.errprint(self.doc.product_test_name)	

		webnotes.conn.sql("""update `tabProduct` set product_test_name='%s' where name='%s'"""%(self.doc.product_test_name,self.doc.name),debug=1)
		webnotes.conn.sql('commit')				