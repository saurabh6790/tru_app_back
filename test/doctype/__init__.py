# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import addchild, Document
from webnotes.utils.email_lib import sendmail
from webnotes.utils import cint, cstr, flt, now, nowdate

def update_test_log(test_details):
	#webnotes.errprint(emp)
	d = Document('Test Log')
	d.sample_no = test_details.get("sample_no")
	d.test = test_details.get("test")
	d.status = test_details.get("workflow_state")
	#webnotes.errprint(d.status)
	d.tester=test_details.get("tested_by")
	d.shift_incharge=test_details.get("shift_incharge")
	d.lab_incharge=test_details.get("lab_incharge")
	d.save()

def verfy_bottle_number(sample_no, bottle_number):
	if bottle_number:
		if cint(webnotes.conn.sql("""select count(*) from tabSample 
			where name='%s' and find_in_set('%s',barcode) """%(sample_no, bottle_number))[0][0]) != 1:
			webnotes.msgprint("Entered bottle number not belongs to Sample No. Please correct it",raise_exception=1)
	else:
		webnotes.msgprint("Please enter bottle number",raise_exception=1)

def assign_notify(test_details):
	#webnotes.errprint(test_details.get("workflow_state"))
	if test_details.get("incharge"):
		#webnotes.errprint(test_details.get("incharge"))
		session_userid = webnotes.conn.sql("select user_id from tabEmployee where name = '%(incharge)s' "%test_details)
		if session_userid:
			create_email(session_userid[0][0],test_details)
			assign_to(session_userid,test_details)


	if test_details.get("workflow_state")=='Rejected':
		#webnotes.errprint("in workflow_state")
		webnotes.conn.sql("update tabSample set status = 'Rejected' where name = '%(sample_no)s' "%test_details)
		webnotes.conn.sql("commit")

def create_test_results(test_detail):
	d = Document("Test Results")
	d.sample_no = test_detail.get("sample_no")
	d.test_name = test_detail.get("test")
	d.test_id= test_detail.get("name")
	if test_detail.get("temperature"):
		d.temperature=test_detail.get("temperature")
	d.save()
	return d.name
	
def create_child_testresult(parent,value,test_detail,label):
	from webnotes.model.doc import get
	if parent and value and label:
		doc = get('Test Results', parent)
		doclist = get('Test Results', parent, with_children=1)
		ch = addchild(doc[0], 'test_result_detail', 'Test Result Details', doclist)
		ch.test_name = test_detail.get("test")
		ch.test_values=value
		ch.parent=parent
		ch.spec_limits = test_detail.get('pgcil_limit')
		ch.test_method = test_detail.get('method')
		ch.particulors_of_test=label
		ch.save()


def create_email(session_userid,test_details):
	msg="Hello, %(test)s=%(name)s is assigned to you please check it in your ToDo List " %test_details

	send_email(session_userid, msg, test_details)


# Send Email Function	
def send_email(email, msg, test_details):
	from webnotes.utils.email_lib import sendmail
	sendmail(email, subject="%(test)s"%test_details, msg = msg)
	

# For creating ToDo Document- Assign To
def assign_to(session_userid,test_details):
	from webnotes.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate
	today = nowdate()
	d = Document("ToDo")
	d.owner = session_userid[0][0]
	d.reference_type = test_details.get("test")
	d.reference_name = test_details.get("name")
	d.priority =  'Medium'
	d.date = today
	d.assigned_by = webnotes.user.name
	d.save(1)

def get_pgcil_limit(method):
	return webnotes.conn.get_value('Test Method', method ,'as_per_pgcil_spec_limits')