# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import addchild, Document
from webnotes import msgprint, _
from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_submit(self):
		self.update_sample_status()

	def update_sample_status(self):
		samples = {}
		for sample in getlist(self.doclist, 'sample_allocation_detail'):
			samples[sample.get('sample_no')] = ''
			self.test_allocation(sample)

		for sample in samples:
			webnotes.conn.sql("update tabSample set status = 'Assigned' where name = '%s'"%sample)
			webnotes.conn.sql("commit")

	def test_allocation(self, sample):
		test_id = self.create_test(sample)
		self.create_todo(sample, test_id)

	def create_test(self, sample):
		test = Document(sample.get("test"))
		test.sample_no = sample.get("sample_no")
		# test.tested_by = sample.get("tester")
		test.shift_incharge_approval = sample.get("shift_incharge")
		test.lab_incharge_approval = sample.get("lab_incharge")
		test.save()
		self.update_test_id(sample,test.name)
		return test.name

	def update_test_id(self,sample,test_name):
		webnotes.errprint("update `tabSample Allocation Detail` set test_id='"+test_name+"' where sample_no='"+sample.get("sample_no")+"' and test='"+sample.get("test")+"' and parent='"+self.doc.name+"'")
		webnotes.conn.sql("update `tabSample Allocation Detail` set test_id='"+test_name+"' where sample_no='"+sample.get("sample_no")+"' and test='"+sample.get("test")+"' and parent='"+self.doc.name+"'")
		webnotes.conn.commit()

	def create_todo(self, sample, test_id):
		user = webnotes.conn.sql("select user_id  from tabEmployee where name = '%s'"%(sample.get("tester")),as_list=1)
		if user:
			d = Document("ToDo")
			d.owner = user[0][0]
			d.reference_type = sample.get("test")
			d.reference_name = test_id
			d.priority =  'Medium'
			d.date = nowdate()
			d.assigned_by = webnotes.user.name
			d.save(1)
		
	def add_samples(self):
		if self.doc.sample_type == 'Single Sample':
			test_details = self.get_sample_wise_test(self.doc.sample_id)
			# self.check_register(self.doc.sample_id)
			self.fill_sample_alloacation_detail(test_details, self.doc.sample_id)

		if self.doc.sample_type == "Batch":
			samples = webnotes.conn.sql("select sample from `tabBatch Detail` bd where bd.parent =  '%s' "%self.doc.batch, as_list=1)
			for sample in samples:
				# self.check_register(sample[0])
				self.fill_sample_alloacation_detail(self.get_sample_wise_test(sample[0]), sample[0])

	def check_register(self, sample_id):
		register_no = webnotes.conn.sql("""select name from tabRegister where sample_no = '%s'"""%(sample_id))
		if not register_no:
			webnotes.msgprint("Registration not yet done for selected sample.",raise_exception=1)

	def get_sample_wise_test(self, sample_id):
		tests = self.check_group_or_other(sample_id)
		if tests:
			return tests
		else:
			return webnotes.conn.sql("""select test from `tabGroup Test` 
				where parent in (select test_required from `tabSample Entry` 
					where name=(select sample_entry from tabSample where name = '%s'))"""%(sample_id),as_list=1)

	def check_group_or_other(self, sample_id):
		test_required = webnotes.conn.sql(""" select test_required, name from `tabSample Entry`
		 where name = (select sample_entry from tabSample where name = '%s')"""%(sample_id))[0][0]
		if test_required == 'Others':
			return webnotes.conn.sql(""" select test from `tabRegister Test Details` where parent = '%s' """%(test_required[0][1]), as_list=1)

	def fill_sample_alloacation_detail(self, sample_details, sample_id):
		if self.doc.sample_id:
			self.doclist=self.doc.clear_table(self.doclist,'sample_allocation_detail')
		for sample in sample_details:
			nl = addchild(self.doc, 'sample_allocation_detail', 'Sample Allocation Detail', self.doclist)
			nl.sample_no = sample_id
			nl.test = sample[0]

def get_samples(doctype, txt, searchfield, start, page_len, filters):
	return webnotes.conn.sql(""" select s.name, se.priority from `tabSample` s,`tabSample Entry` se 
		where ifnull(s.status,'') not in ('Assigned') and s.sample_entry = se.name """)

def get_employee(doctype, txt, searchfield, start, page_len, filters):
	conditions = make_condition(filters)
	return webnotes.conn.sql(""" select parent from `tabEmployee Training Details` where 
		%(key)s like "%(txt)s" and %(cond)s  
		limit %(start)s, %(page_len)s """%{'key': searchfield, 'txt': "%%%s%%" % txt, 
		'cond': conditions, 'start': start, 'page_len': page_len})

def make_condition(filters):
	cond = ''

	if filters.get("level"):
		cond += " level = '%(level)s'"%{'level': filters.get("level")}

	if filters.get("test"):
		cond += " and test = '%(test)s'"%{'test': filters.get("test")}

	if filters.get("parent"):
		if isinstance(filters.get("parent"), list):
			parent = "('%s', '%s')"%(filters.get("parent")[0], filters.get("parent")[1])
			cond += " and parent not in %(parent)s"%{'parent':parent}
		else:
			cond += " and parent != '%s'"%filters.get('parent')

	return cond 