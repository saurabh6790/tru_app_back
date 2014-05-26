cur_frm.add_fetch('sample_no', 'barcode', 'bottle_no');


cur_frm.fields_dict.sample_no.get_query = function(doc, cdt, cdn) {
	return{
		query:"test.doctype.register.register.get_samples"
	}
}

// cur_frm.cscript.others = function(doc,cdt,cdn){
// 	if(doc.sample_no){
//     //console.log("in employee trigger")
// 	 	get_server_fields('get_test_details','','',doc,cdt,cdn,1,function(r,rt){refresh_field('test_details')});
//  	}
//  	else
//  		msgprint("Sample No Can Not Be Blank...")
 	
// }