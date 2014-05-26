# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import Document

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def on_submit(self):
		if self.doc.approver:
			self.assign_to()
		else:
			webnotes.msgprint("Mention Approver First",raise_exception=1)


	def assign_to(self):
		from webnotes.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate
		#webnotes.errprint(self.doc.approver)
		today = nowdate()
		d = Document("ToDo")
		d.owner = self.doc.approver
		d.reference_type = "Request"
		d.reference_name = self.doc.name
		d.priority =  'Medium'
		d.date = today
		d.assigned_by = webnotes.user.name
		d.save(1)
		#webnotes.errprint(d)