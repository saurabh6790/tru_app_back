# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint, cstr, flt, now, nowdate
from webnotes.model.doc import Document, addchild
from webnotes.utils.email_lib import sendmail
from webnotes import msgprint, _

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def generate_sample_id(self):
		self.generate_sample()
		self.update_sample_entry()
		# if self.doc.no_of_sample_id:

			# serialno=webnotes.conn.sql("select serial_no from `tabStock Entry Detail` where parent='%s'"%(self.doc.stock_e),as_list=1)
			# serialno_list=serialno[0][0].split('\n')

			# start = 0
			# end = len(serialno_list)/cint(self.doc.no_of_sample_id)

			# sample_list = []
			# for i in range(0,cint(self.doc.no_of_sample_id)):
			# 	if i != cint(self.doc.no_of_sample_id)-1:
			# 		sample_list.append(serialno_list[start:end])
			# 	else:
			# 		sample_list.append(serialno_list[start:len(serialno_list)])
			# 	start = end
			# 	end = end+len(serialno_list)/cint(self.doc.no_of_sample_id)

			# self.generate_sample(sample_list)
			# self.update_stock_entry()
		webnotes.msgprint("New Samples are generated. Please Save(Ctrl+S) before leaving form")

		# else:
		# 	webnotes.msgprint("Please mention No. Of Sample Id First..",raise_exception=1)

	def generate_sample(self):
		samples = {}
		# for sample in sample_list:
		d = Document("Sample")
		d.sample_entry = self.doc.s_entry
		d.barcode = self.doc.bottles_barcodes
		d.save()
		samples[d.name] = self.doc.bottles_barcodes

		self.fill_child_entry(samples)
		
	def fill_child_entry(self, samples):
		self.doclist=self.doc.clear_table(self.doclist,'sample_creation_item_details')

		for sample in samples:
			ch = addchild(self.doc, 'sample_creation_item_details', 
						'Sample Creation Item Details', self.doclist)
			ch.sample_id = sample
			ch.barcode = samples[sample]

	def update_sample_entry(self):
		webnotes.conn.sql("update `tabSample Entry` set sample_generated='Yes' where name='%s'"%self.doc.s_entry)
		webnotes.conn.sql("commit")
		
	def get_sample_entry_details(self,s_entry):
		#webnotes.errprint(s_entry)
		details=webnotes.conn.sql("select bottle_no,bottles_barcodes from `tabSample Entry` where name='"+s_entry+"'",as_list=1)
		#webnotes.errprint(details)
		return {
			'bottle_no':details[0][0],
			'bottles_barcodes':details[0][1]
		}