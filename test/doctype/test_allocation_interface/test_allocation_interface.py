# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.model.doc import addchild
from webnotes.model.doc import Document
from webnotes.model.bean import getlist
from webnotes.model.doc import getchildren
import webnotes


class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	#Select sample details from the sample table to fill all the details in the child table 'Test Allocation Details'
	def get_sample_allocation_details(self,sample_no):

		sample_details=webnotes.conn.sql("select barcode,client_name from `tabSample` where name='"+sample_no+"'",as_list=1)
		for p in getlist(self.doclist, 'test_allocation_detail'):
			if p.sample_no==self.doc.sample_no:
				webnotes.msgprint("You have already selected sample ID='"+self.doc.sample_no+"' Now,please choose any other sample ID",raise_exception=1)
		for i in sample_details:
			#webnotes.errprint(i[0])	
			#webnotes.errprint(i[1])
			ch = addchild(self.doc, 'test_allocation_detail', 
					'Test Allocation Detail', self.doclist)
			ch.sample_no=sample_no
			ch.bottle_no=i[0]
			ch.client_name=i[1]
			ch.save(new=1)


	#Select all the test from the specified test group and add it to the child table 'Test Names'.
	def get_test_details(self,test_group):

		test=webnotes.conn.sql("select test from `tabGroup Test` where parent='"+test_group+"'",as_list=1)
		self.doclist=self.doc.clear_table(self.doclist,'test')

		for j in test:

			cd = addchild(self.doc, 'test', 
					'Test', self.doclist)
			cd.test_name=j
			cd.save(new=1)


	#On clicking button Generate Final Result Table,add combination of selected sample numbers with the specified test 
	def get_finaltest_details(self):
		self.doclist=self.doc.clear_table(self.doclist,'final_test')

		for d in getlist(self.doclist, 'test_allocation_detail'):

			for t in getlist(self.doclist,'test'):
				#webnotes.errprint(t)
				cr =addchild(self.doc,'final_test','Final Test Allocation Detail',self.doclist)
				cr.sample_no=d.sample_no
				cr.bottle_no=d.bottle_no
				cr.priority=d.priority
				cr.specification=d.specification
				cr.client_name=d.client_name
				cr.test=t.test_name
				cr.save(new=1)

	#On clicking on button  Submit Test allocation record created
	def set_test_allocation(self):
		test_list = []
		sample_dict = {}
		local_sample_no = ''

		for t in getlist(self.doclist,'final_test'):
			if local_sample_no == t.sample_no:
				self.create_test_list(t, sample_dict)
			else:
				test_list = []
				local_sample_no = t.sample_no
				self.create_sample_dict(t, sample_dict, test_list)

		self.create_test_allocation(sample_dict)
		webnotes.msgprint("Test Allocation Completed Successfully...!!")

	#To Create sample details dictionary
	def create_sample_dict(self, sample, sample_dict, test_list):
		sample_dict.setdefault(sample.sample_no, {})

		sample_dict[sample.sample_no]['sample_no'] = sample.sample_no
		sample_dict[sample.sample_no]['bottle_no'] = sample.bottle_no
		sample_dict[sample.sample_no]['priority'] = sample.priority
		sample_dict[sample.sample_no]['specification'] = sample.specification
		sample_dict[sample.sample_no]['test_group'] = self.doc.test_group

		test_list.append(sample.test)
		sample_dict[sample.sample_no]['test'] = test_list

	def create_test_list(self, sample, sample_dict):
		sample_dict[sample.sample_no]['test'].append(sample.test)

	#Create Record for Test Allocation
	def create_test_allocation(self, sample_dict):
		if sample_dict:
			for sample in sample_dict:
				parent = self.create_parent(sample_dict[sample])
				self.create_child(parent, sample_dict[sample]['test'])

	def create_parent(self, sample_dict):

		d = Document('Test Allocation')
		d.sample_no = sample_dict['sample_no']
		d.bottle_no = sample_dict['bottle_no']
		d.priority = sample_dict['priority']
		d.specification = sample_dict['specification']
		d.group_name = sample_dict['test_group']
		d.docstatus = 1
		d.save()
		self.update_sample_master(sample_dict)
		return d.name

	def create_child(self, parent, test_list):
		for test in test_list:
			d = Document('Register Test Name')
			d.test_name = test
			d.parent = parent
			d.save()


	#After completing test allocation set status of sample number to the 'Ready To Lab Entry'
	def update_sample_master(self, sample):
		d = Document('Sample', sample['sample_no'])
		d.priority = sample['priority']
		d.specification = sample['specification']
		d.status='Ready To Lab Entry'
		d.save()

def sample_query(doctype, txt, searchfield, start, page_len, filters):
	return webnotes.conn.sql(""" select name from tabSample 
		where status is null 
		and %(key)s like '%(txt)s'"""%{'key':searchfield, 'txt':'%%%s%%'%txt}, debug=1)


#To go from test allocation to the sample allocation to lab
@webnotes.whitelist()
def create_sample_allocation_to_lab(source_name, target_doclist=None):
	#webnotes.errprint(source_name)
	return _create_sample_allocation_to_lab(source_name, target_doclist)



def _create_sample_allocation_to_lab(source_name, target_doclist=None, ignore_permissions=False):
	from webnotes.model.mapper import get_mapped_doclist


	doclist = get_mapped_doclist("Test Allocation Interface", source_name, {
			"Test Allocation Interface": {
				"doctype": "Sample Allocation To Lab", 
								
				"validation": {
					"docstatus": ["=", 0]
				}
			}
	},target_doclist)

	return [d.fields for d in doclist]


