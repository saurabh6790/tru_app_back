#0 Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.model.doc import addchild
from webnotes.model.doc import Document
from webnotes.model.bean import getlist
from webnotes.model.doc import getchildren
from webnotes.utils import cint, cstr, flt, now, nowdate

import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_submit(self):
		self.update_sample_status()


	#Update sample status to the Lab Entry after completing the sample allocation to lab stage.
	def update_sample_status(self):
		for sample in getlist(self.doclist, 'final_sample_allocation'):
			webnotes.conn.sql("update tabSample set status = 'Lab Entry' where name ='"+sample.sample_no+"'")
			webnotes.conn.sql("commit")
			


	#Select sample details from sample table with respect to the priority & quantity specified.
	def get_sample_details(self,priority):
		#n=0
		if priority=='Critical':
			sample_details=webnotes.conn.sql("select name, barcode from `tabSample` where priority='"+priority+"' and status='Ready To Lab Entry' ",as_list=1)

		elif priority=='Normal':
			sample_details=webnotes.conn.sql("select name, barcode from `tabSample` where priority='"+priority+"' and status='Ready To Lab Entry'",as_list=1)
		else:
			sample_details=webnotes.conn.sql("select name, barcode from `tabSample` where priority='"+priority+"' and status='Ready To Lab Entry'",as_list=1)
		if self.doc.flag1==0 and self.doc.priority=='Critical':
				webnotes.msgprint("Sorry--!!! You have Already choose priority='"+priority+"' please choose any other priority",raise_exception=1)
		elif self.doc.flag2==1 and self.doc.priority=='Normal':
				webnotes.msgprint("Sorry--!!! You have Already choose priority='"+priority+"' please choose any other priority",raise_exception=1)
		elif self.doc.flag3==2 and self.doc.priority=='Urgent':
				webnotes.msgprint("Sorry--!!! You have Already choose priority='"+priority+"' please choose any other priority",raise_exception=1)			
		else:

			for i in sample_details:
					test=webnotes.conn.sql("select group_concat(b.test_name),a.group_name from `tabTest Allocation` a,`tabRegister Test Name` b where a.name=b.parent and sample_no='"+i[0]+"'")
					#webnotes.errprint(test[0][1])
					if test:
						ch = addchild(self.doc, 'prioritywise_sample_allocation', 
						'Priority Wise Sample Allocation', self.doclist)
						ch.priority = priority
						ch.sample_no=i[0]
						ch.bottle_no=i[1]
						ch.test=test[0][0]
						ch.test_group=test[0][1]
						ch.save(new=1)
					else:
						webnotes.msgprint("There is no any record against current sample No in Test Allocation")
			if priority=='Critical':

				return{
						'flag1':0
				}
				
			elif priority=='Normal':
				return{
						'flag2':1
				}
			else:
				return{
						'flag3':2
				}


	#Add sample number details according to the specified quantity and priority
	def get_prioritywise_details(self):

		list1=[]
		list2=[]
		list3=[]
		if self.doc.critical_samples and self.doc.normal_samples and self.doc.urgent_samples:

			for p in getlist(self.doclist, 'prioritywise_sample_allocation'):
				#webnotes.errprint(x.priority)
				if p.priority=='Critical':
					list1.append(p.priority)
					
				elif p.priority=='Normal':
					list2.append(p.priority)
				else:
					list3.append(p.priority)
			if cstr(len(list1))<= self.doc.critical_samples:

				if cstr(len(list2))<= self.doc.normal_samples:

					if cstr(len(list3))<= self.doc.urgent_samples:
						pass
					else:
						webnotes.msgprint("Number Of smples having priority 'Urgent' is not equal to or less than the specified quantity of samples for this priority",raise_exception=1)

				else:
					webnotes.msgprint("Number Of smples having priority Normal is not equal to the specified quantity of samples for this priority",raise_exception=1)


			else:
				webnotes.msgprint("Number Of smples having priority Critical is not equal to the specified quantity of samples for this priority",raise_exception=1)


			self.doclist=self.doc.clear_table(self.doclist,'final_sample_allocation')

			for d in getlist(self.doclist, 'prioritywise_sample_allocation'):
				#webnotes.errprint(d)
				cd =addchild(self.doc,'final_sample_allocation','Final Sample Allocation To Lab',self.doclist)
				cd.priority=d.priority
				cd.sample_no=d.sample_no
				cd.bottle_no=d.bottle_no
				cd.test_group=d.test_group
				cd.test=d.test
				cd.save(new=1)
			


#To map sample allocation to lab page to the Sample allocation to Tester page 
@webnotes.whitelist()
def sample_allocation_to_tester(source_name, target_doclist=None):
	
	return _sample_allocation_to_tester(source_name, target_doclist)



def _sample_allocation_to_tester(source_name, target_doclist=None, ignore_permissions=False):

	from webnotes.model.mapper import get_mapped_doclist
	# webnotes.errprint(source_name)
	def postprocess(source, doclist):
		#webnotes.errprint(source_name)
 		doclist[0].sample_allocation_lab= source_name
	doclist = get_mapped_doclist("Sample Allocation To Lab", source_name, {
			"Sample Allocation To Lab": {
				"doctype": "Sample Allocation", 
								
				"validation": {
					"docstatus": ["=", 1]
				}
			}
	},target_doclist ,postprocess)

	return [d.fields for d in doclist]



#Get count of samples according to the priority
@webnotes.whitelist()
def get_count():
	#webnotes.errprint("in get count")
	count_dict = {'Normal': 0,'Urgent': 0,'Critical': 0}

	counts=webnotes.conn.sql("select priority,count(priority) from `tabSample` where status='Ready To Lab Entry' group by priority",as_list=1)
	# webnotes.errprint(counts)
	# webnotes.errprint(len(counts))

	for i in counts:
			count_dict[i[0]] = i[1]

	#webnotes.errprint(count_dict)

	
	return [[k, v] for k, v in count_dict.iteritems()]

