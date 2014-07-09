# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import addchild, Document
from webnotes.utils import cstr, cint, flt, comma_or, nowdate,add_months,getdate,add_days

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def  get_test_details(self):
		#webnotes.errprint("in details")
		self.doclist=self.doc.clear_table(self.doclist,'test_details')
		tests=webnotes.conn.sql("select test_name from `tabTest Name`",as_list=1)
		for i in tests:
			# webnotes.errprint("test")
			ch = addchild(self.doc, 'test_details', 
				'Register Test Details', self.doclist)
			ch.test = i
			ch.save(new=1)

	def validate(self):
		pass
		# self.check_date()


	def check_date(self):
		if getdate(self.doc.date_of_filteration) > getdate(self.doc.date):
			pass
		else:
			webnotes.msgprint("Date of Filteration must be greater than the date of sample collected")
			raise Exception



@webnotes.whitelist()
def make_sample_id(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _make_sample_id(source_name, target_doclist)

def _make_sample_id(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist
	mi=webnotes.conn.sql("select bottle_no,bottles_barcodes from `tabSample Entry` where name='"+source_name+"'")
	#webnotes.errprint(mi[0][1])
	# For Field Mapping From Previous doctype to next doctype
	def postprocess(source, doclist):
		doclist[0].s_entry = source_name
		doclist[0].bottle_no = mi[0][0]
		doclist[0].bottles_barcodes=mi[0][1]
		
	doclist = get_mapped_doclist("Sample Entry", source_name, {
			"Sample Entry": {
				"doctype": "Sample Creation", 
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist, postprocess)

	return [d.fields for d in doclist]