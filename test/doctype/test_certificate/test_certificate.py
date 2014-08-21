# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import addchild, Document
from webnotes.model.bean import getlist


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	# def on_update(self):
	# 	self.check_entries()

	# def check_entries(self):
	# 	webnotes.errprint("in check entries details")
	# 	for g in getlist(self.doclist,'certificate_test_details'):
	# 		webnotes.errprint(g)
	# 	for i in getlist(self.doclist,'other_chrges'):
	# 		webnotes.errprint(i)


	def get_details(self):
		self.fill_parent_details()
		self.child_table()
		return "Done"


	def fill_parent_details(self):
		sample_entry=webnotes.conn.get_value('Sample',self.doc.sample_no,'sample_entry')
		if sample_entry:
			self.doc.sr_no=webnotes.conn.get_value('Sample Entry',sample_entry,'transformer')
			self.doc.rating=webnotes.conn.get_value('Sample Entry',sample_entry,'rating')
			self.doc.ratio=webnotes.conn.get_value('Sample Entry',sample_entry,'voltage_ratio')
			self.doc.make=webnotes.conn.get_value('Sample Entry',sample_entry,'make')

	def child_table(self):
		test_result=webnotes.conn.sql("select a.*,b.temperature from `tabTest Result Details` a, `tabTest Results` b where b.sample_no='%s' and a.parent=b.name order by a.particulors_of_test"%(self.doc.sample_no),as_dict=1)
		self.doclist = self.doc.clear_table(self.doclist, 'certificate_test_details')
		for data in test_result:
			if not data['test_name']=='Resistivity and Dissipation':
				self.create_child_certificate(data['particulors_of_test'],data['test_method'],data['spec_limits'],data['test_values'])
			elif data['particulors_of_test']=='Dielectric Dissipation Factor' or data['particulors_of_test']=='Specific Resistivity':
				particulors_of_test=data['particulors_of_test'] +' @ temp '+data['temperature']
				self.create_child_certificate(particulors_of_test,data['test_method'],data['spec_limits'],data['test_values'])

	def create_child_certificate(self,particulors_of_test,test_method,spec_limits,test_values):
		ch = addchild(self.doc, 'certificate_test_details', 'Certificate Test Details', self.doclist)
		ch.test_values=test_values
		ch.particulors_of_test=particulors_of_test
		ch.spec_limits=spec_limits
		ch.test_method=test_method

	def on_submit(self):
		webnotes.conn.sql("update `tabSample` set docstatus=2 where name='%s'"%self.doc.name,as_list=1)
		webnotes.conn.sql("commit")

	def calculate_voltage(self):
		webnotes.errprint("in create voltage")
		