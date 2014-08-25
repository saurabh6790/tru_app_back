
// cur_frm.fields_dict.sample_allocation_detail.grid.get_field("tester").get_query = function(doc,cdt,cdn)
// {	
//   var d = locals[cdt][cdn];
//   return {
// 		query: "test.doctype.sample_allocation.sample_allocation.get_employee",
// 		filters: {
// 			//"level": 'Level 1',
// 			"test": d.testtest_method, specification = self.get_test_method(sample)
// 				test = Document(tests[0])
// 				test.sample_no = sample.get("sample_no")
// 				test.specification = specification
// 				test.temperature = webnotes.conn.get_value('Sample', self.doc.sample_no, 'temperature')
// 				test.tested_by = self.doc.tester
// 				test.save()
// 				self.update_test_id(sample,test.name)
// 				retu,
// 			"tester":d.tester
// 		}
// 	}
// }



cur_frm.fields_dict['sample_no'].get_query=function(doc,cdt,cdn)
{	
	console.log(doc.sample_no);
	return{
		query:"test.doctype.sample_allocation.sample_allocation.get_sample_no",
		// filters: {
		// 	"samp_no":doc.sample_no
		// }
		
	}
}

cur_frm.cscript.add_test = function(doc,cdt,cdn){
	if (doc.test_name && doc.sample_allocation_lab){
		get_server_fields('get_sample_no','','',doc,cdt,cdn,1,function(r,rt){refresh_field('sample_allocation_detail')});

	}
	else
		msgprint("To add entries in the child table both the fields,Test Name & Sample Allocation To Lab Name must be specify");
}

//cur_frm.add_fetch('sample_no', 'priority', 'priority');


cur_frm.cscript.sample_no = function(doc,cdt,cdn){
	if(doc.sample_no){
		get_server_fields('get_sample_details',doc.sample_no,'',doc,cdt,cdn,1,function(r,rt){refresh_field('sample_allocation_detail')});
		refresh_field('s_priority');
		refresh_field('bottle_no');
		refresh_field('test_group');
	}

}


// cur_frm.get_field("test_name").get_query=function(doc,cdt,cdn){

//   return "select test from `tabFinal Sample Allocation To Lab` where parent='"+doc.sample_allocation_lab+"'" 

// }

// cur_frm.fields_dict.sample_allocation_detail.grid.get_field("shift_incharge").get_query = function(doc,cdt,cdn)
// {
  
//   var d = locals[cdt][cdn];
//   return {
// 		query: "test.doctype.sample_allocation.sample_allocation.get_employee",
// 		filters: {
// 			"level": 'Level 2',
// 			"test": d.test,
// 			"parent": d.tester
// 		}
// 	}
// }

// cur_frm.fields_dict.sample_allocation_detail.grid.get_field("lab_incharge").get_query = function(doc,cdt,cdn)
// {	
//   var d = locals[cdt][cdn];	
//   return {
// 		query: "test.doctype.sample_allocation.sample_allocation.get_employee",
// 		filters: {
// 			"level": 'Level 3',
// 			"test": d.test,
// 			"parent": [d.tester, d.shift_incharge]
// 		}
// 	}
// }

// cur_frm.fields_dict.sample_no.get_query = function(doc, cdt, cdn) {
// 	console.log("hii");
// 	return{
// 		query:"test.doctype.sample_allocation.sample_allocation.get_samples",
// 		filters: {
// 			"sample_no": doc.sample_no
// 		}
// 	}
// }



