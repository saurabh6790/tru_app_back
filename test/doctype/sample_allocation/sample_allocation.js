
// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



cur_frm.fields_dict['sample_no'].get_query=function(doc,cdt,cdn)
{	
	return{
		query:"test.doctype.sample_allocation.sample_allocation.get_sample_no",
	}
}

cur_frm.fields_dict.test_name.get_query = function(doc, cdt, cdn){
	return{
		query:"test.doctype.sample_allocation.sample_allocation.get_test_name",
		filters:{'sample_allocation_id': doc.sample_allocation_lab}
	}
}

//Add selected test to the sample allocation table iff that test is allocated in sample allocation to lab 
cur_frm.cscript.add_test = function(doc,cdt,cdn){
	if (doc.test_name && doc.sample_allocation_lab){
		get_server_fields('get_sample_no','','',doc,cdt,cdn,1,function(r,rt){refresh_field('sample_allocation_detail')});

	}
	else
		msgprint("To add entries in the child table both the fields,Test Name & Sample Allocation To Lab Name must be specify");
}



cur_frm.cscript.sample_no = function(doc,cdt,cdn){
	if(doc.sample_no){
		get_server_fields('get_sample_details',doc.sample_no,'',doc,cdt,cdn,1,function(r,rt){refresh_field('sample_allocation_detail')});
		refresh_field('s_priority');
		refresh_field('bottle_no');
		refresh_field('test_group');
	}

}

