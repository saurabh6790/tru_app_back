# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
from webnotes.model.doc import Document, make_autoname

import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def validate(self):
		self.get_equipmentid_record()

	def get_equipmentid_record(self):
		#webnotes.errprint(self.doc.equipment_id)
		eid=webnotes.conn.sql("select name from `tabTransformer` where equipment_id='"+self.doc.equipment_id+"'",as_list=1)
		if eid:
			webnotes.msgprint("Equipment ID which you select is aleready assign in Transformer Entry='"+eid[0][0]+"'",raise_exception=1)
		else:
			pass


	def get_new_equipmentid(self,args):
		dic=eval(args)
		d = Document("Reporting Person History")
		d.ad_type='Transformer'
		d.plant=(dic['plant'])
		d.client = (dic['client'])
		d.sub_station= (dic['sub station'])
		d.functional_location=(dic['functional_location'])
		d.equipment_id=(dic['equipment_id'])
		d.save()
		return{
		"equipment_id":'',
		"sample_no":'',
		"make":'',
		"rating":'',
		"ratio":'',
		"phase":'',
		"year_of_mfg":'',
		"serial_no":'',
		"voltage_ratio":''
		}