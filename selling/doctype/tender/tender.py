# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_submit(self):
		webnotes.conn.sql("""update `tabQuotation` set tender_name='%s'
	 		where name='%s'"""%(self.doc.name, self.doc.quotation_name))
		webnotes.conn.sql('commit')	
