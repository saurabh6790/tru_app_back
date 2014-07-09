# # Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# # MIT License. See license.txt

# # For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import addchild, Document
from webnotes import msgprint, _
from webnotes.model.bean import getlist
from webnotes.utils import cint, cstr, flt, now, nowdate, get_first_day, get_last_day, add_to_date, getdate

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl     

	def get_sample_details(self,sample_no):
		tests=None
		sample_details=webnotes.conn.sql("""select priority,bottle_no,test_group 
				from `tabFinal Sample Allocation To Lab` 
			where sample_no='%(sample_no)s'"""%{'sample_no':sample_no})
		
		if sample_details:
			if sample_no in webnotes.conn.sql("""select distinct sample_no 
				from `tabTest Log`""", as_list=1)[0]:

				tests=webnotes.conn.sql("""select group_concat(test)
					from `tabTest Log` where sample_no='%(sample_no)s'
				"""%{'sample_no':sample_no})
				webnotes.errprint(tests)

			else:
				tests=webnotes.conn.sql("""select test 
					from `tabFinal Sample Allocation To Lab` 
				where sample_no='%(sample_no)s'"""%{'sample_no':sample_no})
				webnotes.errprint(['else',tests])
		
		if tests:
			test=tests[0][0].split(',')
			webnotes.errprint(test)
			if test:
				self.doclist=self.doc.clear_table(self.doclist,'sample_allocation_detail')
				for i in test:
					#webnotes.errprint(i)
					ch = addchild(self.doc, 'sample_allocation_detail', 
							'Sample Allocation Detail', self.doclist)
					ch.test=i
					ch.save(new=1)

		return{
		"s_priority":sample_details[0][0] if sample_details else '',
		"bottle_no":sample_details[0][1] if sample_details else '',
		"test_group":sample_details[0][2] if sample_details else ''
		}
	
	def on_submit(self):
		#webnotes.errprint("in on update")
		self.update_sample_status()

	def get_sample_no(self):
		samples=webnotes.conn.sql("""select sample_no from `tabFinal Sample Allocation To Lab` 
			where parent='%s' and find_in_set('%s',test) """ %(self.doc.sample_allocation_lab,self.doc.test_name),as_list=1)
		#webnotes.errprint(samples[0])
		if samples:
			for [sample_no] in samples:
				webnotes.errprint(sample_no)
				sample_detail=webnotes.conn.sql("""select barcode,priority from `tabSample` 
					where name='%s'"""%(sample_no),as_list=1)
				webnotes.errprint(sample_detail)
				for d in getlist(self.doclist, 'sample_allocation_detail'):
					if d.sample_no==sample_no:
						webnotes.errprint(d.sample_no)
						webnotes.errprint(sample_no)
						if d.test:
							d.test = d.test + ', ' +self.doc.test_name 
						else:
							d.test = self.doc.test_name
						return{	
							"test": d.test,
							"test_name":''
						}

				ch = addchild(self.doc, 'sample_allocation_detail', 
					'Sample Allocation Detail', self.doclist)
				#webnotes.errprint(ch)
				ch.sample_no=sample_no
				ch.test=self.doc.test_name
				ch.bottle_no=sample_detail[0][0]
				ch.priority=sample_detail[0][1]
				ch.save(new=1)
		else:
			webnotes.msgprint("There is no any Samle Number allocated aginst the test='"+self.doc.test_name+"'",raise_exception=1)
			return{
				"test_name":''
			}


		return{
			"test_name": ''
		}

	def update_sample_status(self):
		#webnotes.errprint("in update sample status")
		samples = {}
		for sample in getlist(self.doclist, 'sample_allocation_detail'):
			#samples[sample.get('sample_no')] = ''
			self.test_allocation(sample)

		#for updation of status in Sample Doctype
		webnotes.conn.sql("update tabSample set status = 'Assigned' where name ='"+self.doc.sample_no+"'")
		webnotes.conn.sql("commit")
		
	def test_allocation(self, sample):
		#webnotes.errprint("in test allocation")

		test_id = self.create_test(sample)
 		self.create_todo(sample, test_id)
 		

	def create_test(self,sample):
		#webnotes.errprint("in create test")
		webnotes.errprint(sample.get("test"))
		test_method, specification = self.get_test_method(sample)
		test = Document(sample.get("test"))
		test.sample_no = sample.get("sample_no")
		#test.method = test_method
		test.specification = specification
		test.temperature = webnotes.conn.get_value('Sample', self.doc.sample_no, 'temperature')
		test.tested_by = self.doc.tester
		test.save()
		self.update_test_id(sample,test.name)
		return test.name

	def get_test_method(self, sample):
		specification = webnotes.conn.get_value("Sample", self.doc.sample_no, 'specification')
		test_method = webnotes.conn.sql("""select test_method from `tabTest Specification` 
			where specification = '%s' and test = '%s'"""%(specification, sample.get("test")))
		return test_method[0][0] if test_method else '', specification

	def update_test_id(self,sample,test_name):
		#webnotes.errprint("in update test id")

		#webnotes.errprint("update `tabSample Allocation Detail` set test_id='"+test_name+"' where sample_no='"+self.doc.sample_no+"' and test='"+sample.get("test")+"' and parent='"+self.doc.name+"'")
		webnotes.conn.sql("update `tabSample Allocation Detail` set test_id='"+test_name+"' where test='"+sample.get("test")+"' and parent='"+self.doc.name+"'")
		webnotes.conn.commit()

	def create_todo(self,sample,test_id):
		#webnotes.errprint("in create todo")
		userid = webnotes.conn.sql("select user_id  from tabEmployee where name = '%s'"%(sample.get("tester")),as_list=1)
		#webnotes.errprint(user[0][0])
		if userid:
			d = Document("ToDo")
			d.owner = userid[0][0]
			d.reference_type = sample.get("test")
			d.reference_name = test_id
			d.priority =  'Medium'
			d.date = nowdate()
			d.assigned_by = webnotes.user.name
			d.save(1)

def get_sample_no(doctype, txt, searchfield, start, page_len, filters):
	
	return 	webnotes.conn.sql(""" select  name from tabSample where status = 'Lab Entry' 
		union select distinct sample_no from`tabTest Log` tl""")

	
# 	def add_samples(self):
# 		if self.doc.sample_type == 'Single Sample':
# 			test_details = self.get_sample_wise_test(self.doc.sample_id)
# 			# self.check_register(self.doc.sample_id)
# 			self.fill_sample_alloacation_detail(test_details, self.doc.sample_id)

# 		if self.doc.sample_type == "Batch":
# 			samples = webnotes.conn.sql("select sample from `tabBatch Detail` bd where bd.parent =  '%s' "%self.doc.batch, as_list=1)
# 			for sample in samples:
# 				# self.check_register(sample[0])
# 				self.fill_sample_alloacation_detail(self.get_sample_wise_test(sample[0]), sample[0])

# 	def check_register(self, sample_id):
# 		register_no = webnotes.conn.sql("""select name from tabRegister where sample_no = '%s'"""%(sample_id))
# 		if not register_no:
# 			webnotes.msgprint("Registration not yet done for selected sample.",raise_exception=1)

# 	def get_sample_wise_test(self, sample_id):
# 		tests = self.check_group_or_other(sample_id)
# 		if tests:
# 			return tests
# 		else:
# 			return webnotes.conn.sql("""select test from `tabGroup Test` 
# 				where parent in (select test_required from `tabSample Entry` 
# 					where name=(select sample_entry from tabSample where name = '%s'))"""%(sample_id),as_list=1)

# 	def check_group_or_other(self, sample_id):
# 		test_required = webnotes.conn.sql(""" select test_required, name from `tabSample Entry`
# 		 where name = (select sample_entry from tabSample where name = '%s')"""%(sample_id))[0][0]
# 		if test_required == 'Others':
# 			return webnotes.conn.sql(""" select test from `tabRegister Test Details` where parent = '%s' """%(test_required[0][1]), as_list=1)

# 	def fill_sample_alloacation_detail(self, sample_details, sample_id):
# 		if self.doc.sample_id:
# 			self.doclist=self.doc.clear_table(self.doclist,'sample_allocation_detail')
# 		for sample in sample_details:
# 			nl = addchild(self.doc, 'sample_allocation_detail', 'Sample Allocation Detail', self.doclist)
# 			nl.sample_no = sample_id
# 			nl.test = sample[0]

# def get_samples(doctype, txt, searchfield, start, page_len, filters):
# 	return webnotes.conn.sql(""" select s.name, se.priority from `tabSample` s,`tabSample Entry` se 
# 		where ifnull(s.status,'') not in ('Assigned') and s.sample_entry = se.name """)


# def get_samples(doctype, txt, searchfield, start, page_len, filters):
# 	webnotes.errprint(filters)
	# return webnotes.conn.sql(""" select s.name, se.priority from `tabSample` s,`tabSample Entry` se 
	# 	where ifnull(s.status,'') not in ('Assigned') and s.sample_entry = se.name """)



def get_employee(doctype, txt, searchfield, start, page_len, filters):
	#webnotes.errprint("hi")
	return webnotes.conn.sql(""" select name, employee_name, date_of_birth from tabEmployee 
		where (%(key)s like "%(txt)s" or employee_name like "%(txt)s")"""%{'key':searchfield, 'txt': "%%%s%%" % txt})
# 	conditions = make_condition(filters)
# 	webnotes.errprint(conditions)
# 	return webnotes.conn.sql(""" select parent from `tabEmployee Training Details` where 
# 		%(key)s like "%(txt)s" and %(cond)s  
# 		limit %(start)s, %(page_len)s """%{'key': searchfield, 'txt': "%%%s%%" % txt, 
# 		'cond': conditions, 'start': start, 'page_len': page_len})

# def make_condition(filters):
# 	cond = ''

# 	# if filters.get("level"):
# 	# 	cond += " level = '%(level)s'"%{'level': filters.get("level")}

# 	if filters.get("test"):
# 		cond += " and test = '%(test)s'"%{'test': filters.get("test")}

# 	# if filters.get("parent"):
# 	# 	if isinstance(filters.get("parent"), list):
# 	# 		parent = "('%s', '%s')"%(filters.get("parent")[0], filters.get("parent")[1])
# 	# 		cond += " and parent not in %(parent)s"%{'parent':parent}
# 	# 	else:
# 	# 		cond += " and parent != '%s'"%filters.get('parent')

# 	return cond 