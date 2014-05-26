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

	def on_submit(self):
		webnotes.conn.sql("update tabSample set status='Registered' where name = '%s' "%(self.doc.sample_no))
		webnotes.conn.sql("commit")

	# def  get_test_details(self):
	# 	#webnotes.errprint("in details")
	# 	self.doclist=self.doc.clear_table(self.doclist,'test_details')
	# 	if self.doc.others==1:
	# 		tests=webnotes.conn.sql("select test_name from `tabTest Name`",as_list=1)
	# 		for i in tests:

	# 			ch = addchild(self.doc, 'test_details', 
	# 				'Register Test Details', self.doclist)
	# 			ch.test = i
	# 			ch.save(new=1)


def get_samples(doctype, txt, searchfield, start, page_len, filters):
	return webnotes.conn.sql(""" select name from `tabSample` 
		where ifnull(status,'') not in ('Assigned', 'Registered', 'Rejected') """)