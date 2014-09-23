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

	def on_submit(self):
		self.update_sample_status()
		self.update_sample_allocation_to_lab()

	#Select test from sample allocation to lab & also from the test log where we kept rejected test
	def get_sample_no(self):
		
		samples=webnotes.conn.sql("""select f.sample_no from `tabFinal Sample Allocation To Lab` f 
		where 
				f.parent='%(parent)s' 
				and find_in_set('%(test_name)s',f.test) 
		union 
			select sample_no from `tabTest Log` tl 
		where 
			test = '%(test_name)s' and docstatus in ('0','1')""" %{'parent':self.doc.sample_allocation_lab, 'test_name':self.doc.test_name },as_list=1)
		if samples:
			for sample_no in samples:
				flag = False
				sample_detail=webnotes.conn.sql("""select barcode,priority from `tabSample` 
					where name='%s'"""%(sample_no[0]),as_list=1)
				for d in getlist(self.doclist, 'sample_allocation_detail'):
					if d.sample_no==sample_no[0]:
						if d.test:
							if not self.doc.test_name in d.test:
								d.test = d.test + ',' +self.doc.test_name 
						else:
							d.test = self.doc.test_name
						flag = True
				if not flag:
					self.create_child_record(sample_no[0], sample_detail)	
		else:
			webnotes.msgprint("There is no any Samle Number allocated against the test='"+self.doc.test_name+"'",raise_exception=1)
			return{
				"test_name":''
			}
		return{
			"test_name": ''
		}

	#To add entries in child table according to the selected test.
	def create_child_record(self, sample_no, sample_detail):
		ch = addchild(self.doc, 'sample_allocation_detail', 
					'Sample Allocation Detail', self.doclist)
		ch.sample_no=sample_no
		ch.test=self.doc.test_name
		ch.bottle_no=sample_detail[0][0]
		ch.priority=sample_detail[0][1]
		ch.save(new=1)

	#To change status of sample to 'Assigned' after completing the sample allocation
	def update_sample_status(self):
		samples, dic = {}, {}
		for sample in getlist(self.doclist, 'sample_allocation_detail'):
			#samples[sample.get('sample_no')] = ''
			self.test_allocation(sample, dic)

		self.prepare_escape_test(dic)

		#for updation of status in Sample Doctype
		for sample in getlist(self.doclist,'sample_allocation_detail'):
			webnotes.conn.sql("update tabSample set status = 'Assigned' where name ='"+sample.sample_no+"'")
			webnotes.conn.sql("commit")

	#To disable link from sample allocation to lab to sample allocation to tester after completing sample allocation to tester process corresponding to the perticular sample allocation to lab form.
	def update_sample_allocation_to_lab(self):
		webnotes.conn.sql("update `tabSample Allocation To Lab` set sample_allocation_name='"+self.doc.name+"' where name ='"+self.doc.sample_allocation_lab+"'")
		webnotes.conn.sql("commit")

	#To create document for each test present in sample allocation detail table.	
	def test_allocation(self, sample, dic):
		self.create_test(sample, dic)
	
	def create_test(self,sample, dic):
		tests=sample.get("test").split(',')
		length=len(tests)
		if length==1:
			single_sample =[]
			self.ckeck_test(tests[0],sample, dic, single_sample)
		else:
			for test in tests:
				test_id = self.ckeck_test(test,sample,dic)

	#Test which involve basic step as Test Preparation 
	def ckeck_test(self, test_name, sample, dic, sample_nos=None):
		escape_tests=['Neutralization Value', 'Sediment','Furan Content','Corrossive Sulphur','Oxidation Stability','Accelerated Aging']
		if test_name not in escape_tests:
			test_id=self.create_doc(test_name, sample)
			self.create_todo(sample, test_name,  test_id)
		else:
			if dic.get(test_name):
				dic[test_name].append(sample.get('sample_no'))
			else:
				dic[test_name] = [sample.get('sample_no')]
			# webnotes.errprint(dic[test_name])

	#create document for escape test.
	def prepare_escape_test(self, dic):
			# dic = {'Test Name':['sample numbers']}
			for test_name in dic:
				parent=self.create_test_preparation(test_name)
				self.create_child_test_preparation(dic[test_name], test_name, parent)
				self.create_todo_preparation(parent,self.doc.tester, test_name)

	#Create Document for escape test i.e document for Test Preparation Form
	def create_test_preparation(self,test_name):
		if test_name == 'Neutralization Value':
			test_preparation = Document("Neutralization Value")
			test_preparation.tested_by = self.doc.tester 
			test_preparation.save() 

		else :
			test_preparation=Document("Test Preparation")
			test_preparation.test=test_name
			test_preparation.save()

		return test_preparation.name

	#add child records in the test preparation form child table.
	def create_child_test_preparation(self, samples, test_name, parent):
		temp = 0
		childtab = {'Neutralization Value':['neutralisation_test_details', 'Neutralization Test Details']}
		from webnotes.model.doc import get
		if parent and samples:
			doc = get('Neutralization Value' if test_name=='Neutralization Value' else 'Test Preparation', parent)
			doclist = get('Neutralization Value' if test_name=='Neutralization Value' else 'Test Preparation', parent, with_children=1)
			for sample in samples:
				ch = addchild(doc[0], childtab.get(test_name)[0] if childtab.get(test_name) else 'sample_details', childtab.get(test_name)[1] if childtab.get(test_name) else 'Sample Preparation Details', doclist)
				ch.sample_no = sample
				ch.bottle_no= webnotes.conn.get_value("Sample", sample, "barcode")
				if test_name != 'Neutralization Value': 
					ch.tester=self.doc.tester 
				ch.save()
				temp = get_temp(sample)
				
			d = Document('Neutralization Value' if test_name=='Neutralization Value' else 'Test Preparation', parent)
			d.temperature = temp
			d.save()

	#Create Document for Test which are not involve in the escape test.
	def create_doc(self, test_name, sample):
		test_method, specification = self.get_test_method(sample)
		test = Document(test_name)
		test.sample_no = sample.get("sample_no")
		test.specification = specification
		test.temperature = get_temp(sample.get("sample_no"))
		test.tested_by = self.doc.tester
		test.save()
		self.update_test_id(sample,test.name)
		return test.name

	def get_test_method(self, sample):
		specification = webnotes.conn.get_value("Sample", self.doc.sample_no, 'specification')
		test_method = webnotes.conn.sql("""select test_method from `tabTest Specification` 
			where specification = '%s' and test = '%s'"""%(specification, sample.get("test")))
		return test_method[0][0] if test_method else '', specification

	def update_test_id(self, sample, test_name):
		webnotes.conn.sql("update `tabSample Allocation Detail` set test_id='"+test_name+"' where test='"+sample.get("test")+"' and parent='"+self.doc.name+"'")
		webnotes.conn.commit()

	# Create TODO Notification for tester.
	def create_todo(self, sample, test_name, test_id):
		# webnotes.errprint("in create to do")
		userid = webnotes.conn.sql("select user_id from tabEmployee where name = '%s'"%(self.doc.tester),as_list=1)
		# webnotes.errprint([userid , sample, sample.get("tester")])
		if userid:
			d = Document("ToDo")
			d.owner = userid[0][0]
			d.reference_type = test_name
			d.reference_name = test_id
			d.priority =  'Medium'
			d.date = nowdate()
			d.assigned_by = webnotes.user.name
			d.save(1)
			# webnotes.errprint(d.name)

	#Create TODO Notification Of Test Preparation for tester.
	def create_todo_preparation(self, parent, tester, test_name):
		# webnotes.errprint("in create to do test preparation")
		d = Document("ToDo")
		d.owner = webnotes.conn.get_value("Employee",tester,'user_id')
		d.reference_type = 'Neutralization Value' if test_name == 'Neutralization Value' else 'Test Preparation'	
		d.reference_name = parent
		d.priority =  'Medium'
		d.date = nowdate()
		d.assigned_by = webnotes.user.name
		d.save(1)	
		

def get_test_name(doctype, txt, searchfield, start, page_len, filters):
	return get_test(filters)

def get_test(filters):
	lst = []

	lab_test = webnotes.conn.sql("""select test from `tabFinal Sample Allocation To Lab` 
			where parent = '%s'"""%(filters.get('sample_allocation_id')), as_list=1)
	
	for test in lab_test:
		for i in test[0].split(','):
			lst.insert(len(lst), [i])

	log_test = webnotes.conn.sql("""select distinct test from `tabTest Log` 
		where docstatus in (0,1) and test is not null""",as_list=1)

	for test in log_test:
		lst.insert(len(lst), [test[0]])

	return map(list, set(map(tuple, lst)))

def get_sample_no(doctype, txt, searchfield, start, page_len, filters):
	return 	webnotes.conn.sql(""" select  name from tabSample where status = 'Lab Entry' 
		union select distinct sample_no from`tabTest Log` tl""")

def get_employee(doctype, txt, searchfield, start, page_len, filters):
	#webnotes.errprint("hi")
	return webnotes.conn.sql(""" select name, employee_name, date_of_birth from tabEmployee 
		where (%(key)s like "%(txt)s" or employee_name like "%(txt)s")"""%{'key':searchfield, 'txt': "%%%s%%" % txt})

def get_temp(sample_no):
	ret = webnotes.conn.sql("""select se.temperature from `tabSample Entry` se, `tabSample` s 
			where se.name = s.sample_entry and s.name = '%s'"""%(sample_no),as_list=1)

	return ((len(ret[0]) > 1) and ret[0] or ret[0][0]) if ret else None