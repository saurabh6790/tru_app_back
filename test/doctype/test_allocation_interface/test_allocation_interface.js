// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


//To add selected sample number in the child table 'Test Allocation Details'
cur_frm.cscript.add = function(doc,cdt,cdn){
  if (doc.sample_no){
    get_server_fields('get_sample_allocation_details',doc.sample_no,'',doc,cdt,cdn,1,function(r,rt){refresh_field('test_allocation_detail')});
	}
}


cur_frm.fields_dict.sample_no.get_query = function(){
  return{ query:"test.doctype.test_allocation_interface.test_allocation_interface.sample_query"}
}


//To fetch all the test names under the specified test group
cur_frm.cscript.test_group = function(doc,cdt,cdn){
  if (doc.test_group){
  	get_server_fields('get_test_details',doc.test_group,'',doc,cdt,cdn,1,function(r,rt){refresh_field('test')});
	}
}

// cur_frm.cscript.clear = function(doc){
//   return wn.ui.toolbar.clear_cache();
// }

//To generate test allocation record 
cur_frm.cscript.final_result = function(doc,cdt,cdn){
  var cl = getchildren('Test Allocation Detail', doc.name, 'test_allocation_detail');
  var cg = getchildren('Test', doc.name, 'test');

  if (cl.length>0 && cg.length>0){
  	get_server_fields('get_finaltest_details','','',doc,cdt,cdn,1,function(r,rt){refresh_field('final_test')});
  }
  else{
		msgprint("To Generate Final Result, Test Allocation Details Table and Test Name Table must be specified.");
  }   
}



//To check whether the final test allocation detail table is empty or not 
cur_frm.cscript.submit = function(doc,cdt,cdn){

  var cl = getchildren('Final Test Allocation Detail', doc.name, 'final_test');

  if (cl.length>0){
    get_server_fields('set_test_allocation','','',doc,cdt,cdn,1);//,function(r,rt){refresh_field('final_test')});
  }
  else
    msgprint("To Generate Document for Test Allocation(Register) Final Test Allocation Detail Table must be specified.");
    
}


//After completing the form entering all the details of test in final table then we done with the test allocation now action link is active to go from test allocation to Sample allocation to lab
cur_frm.cscript.refresh=function(doc,cdt,cdn){
  var cl = getchildren('Final Test Allocation Detail', doc.name, 'final_test');
  if (cl.length>0) {
      cur_frm.add_custom_button(wn._('Create Sample Allocation To Lab'),
      cur_frm.cscript['Create Sample Allocation To Lab']);

    }
}



//Method to map the test allocation interface page to the sample allocation to lab page
cur_frm.cscript['Create Sample Allocation To Lab'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.test_allocation_interface.test_allocation_interface.create_sample_allocation_to_lab",
    source_name: cur_frm.doc.name
  })

}
