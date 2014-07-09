# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import addchild
from webnotes.model.doc import Document
from webnotes.utils.email_lib import sendmail
from webnotes.utils import cint, cstr, flt, now, nowdate
from webnotes.model.doc import Document
from webnotes.utils import nowdate
from webnotes import msgprint, _
from webnotes.utils.email_lib import sendmail
class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):

		#For Sending Mail when status is Cancelled or Re-Scheduled
		if (self.doc.training_status=='Cancelled' or 'Re-Scheduled') and self.doc.training_status!=None:
			user12=webnotes.conn.sql("select user_id from `tabTrainners Details` where parent='"+self.doc.name+"'",as_list=1)
			canceltest=webnotes.conn.sql("select test from `tabTraining Details` where parent='"+self.doc.name+"'",as_dict=1)
			emailmsg="Hello All,A training section for current test '"+cstr(canceltest)+"'   has been '"+self.doc.training_status+"'"
			if user12:
				for t in user12:
					sendmail(t, subject="Training Details", msg = emailmsg)
					#webnotes.msgprint("Message Sent Successfully..!!")
			empid=webnotes.conn.sql("select user_id from `tabEmployee` where employee='"+self.doc.employee+"'",as_list=1)
			if empid:
				sendmail(empid[0][0], subject="Training Details", msg = emailmsg)






	def get_training_details(self):
		# For accessing test details according to the level types
		self.check_record_exit();
		
	def check_record_exit(self):

		
		# For Level 1
		if self.doc.training_level=='Level 1':
			#webnotes.errprint("py file")
			training=webnotes.conn.sql("select name from `tabTraining` where employee='"+self.doc.employee+"' and training_level='Level 1' ")
			#webnotes.errprint(training)
			if training:
				#webnotes.errprint("in training")
				testname=webnotes.conn.sql("select name from `tabTest Name` where name not in (select test from `tabEmployee Training Details`  where parent='"+self.doc.employee+"' and level='Level 1')")
				#webnotes.errprint(qr)
				self.doclist=self.doc.clear_table(self.doclist,'training')
				self.create_document(testname);
			else:
				level0=webnotes.conn.sql("select name from `tabTraining` where employee='"+self.doc.employee+"' and training_level='Level 0' ")
				if level0:

					test=webnotes.conn.sql("select name from `tabTest Name` where employee_type='"+self.doc.e_type+"'",as_list=1,debug=1)
					#webnotes.errprint(test)
					self.create_document(test);
				else:
					webnotes.msgprint("For applying Training Level 1 ,Level 0 Training Must be completed For Employee='"+self.doc.employee+"'",raise_exception=1)



		#For Level 2
		if self.doc.training_level=='Level 2':
			training1=webnotes.conn.sql("select name from `tabTraining` where employee='"+self.doc.employee+"' and training_level='Level 1' ")
			if training1:
				level2=webnotes.conn.sql("select test from `tabEmployee Training Details`  where parent='"+self.doc.employee+"' and level='Level 1' ")
				#webnotes.errprint(qr)
				self.doclist=self.doc.clear_table(self.doclist,'training')
				self.create_document(level2);
			else:
				webnotes.msgprint("For applying Training Level 2 ,Level 1 Training Must be completed For Employee='"+self.doc.employee+"'",raise_exception=1)


		#For Level 3 
		if self.doc.training_level=='Level 3':
			training2=webnotes.conn.sql("select name from `tabTraining` where employee='"+self.doc.employee+"' and training_level='Level 2' ")
			if training2:
				level3=webnotes.conn.sql("select test from `tabEmployee Training Details`  where parent='"+self.doc.employee+"' and level='Level 2' ")
				#webnotes.errprint(qr)
				self.doclist=self.doc.clear_table(self.doclist,'training')
				self.create_document(level3);
			else:
				webnotes.msgprint("For applying Training Level 2 ,Level 1 Training Must be completed For Employee='"+self.doc.employee+"' ",raise_exception=1)


			


	# For adding child entries in Training Details child table in Training DocType
	def create_document(self,test_name):
		self.doclist=self.doc.clear_table(self.doclist,'training')
		if test_name:
			for i in test_name:
				ch = addchild(self.doc, 'training', 
					'Training Details', self.doclist)
				ch.test = i
				ch.save(new=1)
				

	#For Updating Table EmployTraining Details In Employee DocType
	def on_submit(self):

		if self.doc.training_status=='Completed' or self.doc.training_status==None:

			tests=webnotes.conn.sql("select test from `tabTraining Details` where is_pass='1' and parent='"+self.doc.name+"' ")
			#webnotes.errprint(tests)
			if tests:
				for j in tests:
					#webnotes.errprint(j[0])
					d=Document('Employee Training Details')
					d.test= j[0]
					d.is_pass= 1
					d.level= self.doc.training_level
					d.parent=self.doc.employee
					d.save()
			self.create_email();
			self.assign_to();
			
			#For Level 0
			if self.doc.training_level=='Level 0':
				self.create_document_level0();

		else:
			webnotes.msgprint("For successful completion of form update Training Status to 'Completed' ",raise_exception=1)


	def create_document_level0(self):	
			#webnotes.errprint("in document")
			c=Document('Employee Training Details')
			c.test= 'Level 0 Completed'
			c.is_pass= 1
			c.level= self.doc.training_level
			c.parent=self.doc.employee
			c.save()


		
#fromr Creating email,msg
	def create_email(self,user=None,msg=None):
		user=webnotes.conn.sql("select user_id from `tabTrainners Details` where parent='"+self.doc.name+"' ",as_list=1)
		#webnotes.errprint(user)
		msg1=webnotes.conn.sql("select test from `tabTraining Details` where parent='"+self.doc.name+"'",as_dict=1)
		msg2=webnotes.conn.sql("select test from `tabTraining Details` where is_pass='1' and parent='"+self.doc.name+"'",as_dict=1)
		msg3=webnotes.conn.sql("select test from `tabTraining Details` where is_pass is null and parent='"+self.doc.name+"'",as_dict=1)
		msg="Hello, Employee '"+self.doc.employee+"' have applied for the tests which are '"+cstr(msg1)+"' and from which he/she cleared tests which are '"+cstr(msg2)+"' and tests which he/she needs to reconduct are '"+cstr(msg3)+"'"
		#webnotes.errprint(msg)
		if user:
			for j in user:
				self.send_email(j,msg)
				#self.create_todo()

		else:
			webnotes.msgprint("set user id for emplpyee in employee table")

	# For creating ToDo Document- Assigning To	

	def assign_to(self):
		userid=webnotes.conn.sql("select user_id from `tabEmployee` where employee='"+self.doc.employee+"'",as_list=1)
		#webnotes.errprint(userid)
		from webnotes.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate
		today = nowdate()
		if userid:
			d = Document("ToDo")
			d.owner = userid[0][0]
			d.reference_type = 'Training'
			d.reference_name = self.doc.name
			d.priority =  'Medium'
			d.date = today
			d.assigned_by = webnotes.user.name
			d.save(1)
		else:
			webnotes.msgprint("Please Mention User Id for the Employe='"+self.doc.employee+"'")


	# Send Email Function	
	def send_email(self,email,msg):
		from webnotes.utils.email_lib import sendmail
		sendmail(email, subject="Training Details", msg = msg)

# For send notification to employee & trainers.
@webnotes.whitelist()
def send_notification(employee,docname,date):
	
	user1=webnotes.conn.sql("select user_id from `tabTrainners Details` where parent='"+docname+"'",as_list=1)
	testname=webnotes.conn.sql("select test from `tabTraining Details` where parent='"+docname+"'",as_dict=1)

	mssg="Hello All,A training section for current test '"+cstr(testname)+"'   has been scheduled on '"+date+"' "
	userid1=webnotes.conn.sql("select user_id from `tabEmployee` where employee='"+employee+"'",as_list=1)

	if user1 and testname:
		
		for k in user1:
			sendmail(k, subject="Training Details", msg = mssg)
	
	if userid1:

		sendmail(userid1[0][0], subject="Training Details", msg = mssg)



