
cur_frm.add_fetch('transformer', 'plant', 'plant');

cur_frm.add_fetch('transformer', 'make', 'make');

cur_frm.add_fetch('transformer', 'rating', 'rating');

cur_frm.add_fetch('transformer', 'voltage_ratio', 'voltage_ratio');

cur_frm.add_fetch('transformer', 'phase', 'phase');

cur_frm.add_fetch('transformer', 'serial_no', 'serial_no');

cur_frm.add_fetch('transformer', 'sub_station', 'sub_station');

cur_frm.add_fetch('transformer', 'functional_location', 'functional_location');

//cur_frm.add_fetch('transformer','point_of_sample','point_of_sample');



cur_frm.cscript.test_required = function(doc,cdt,cdn){
	if(doc.test_required == 'Others'){
    //console.log("in employee trigger")
	 	get_server_fields('get_test_details','','',doc,cdt,cdn,1,function(r,rt){refresh_field('test_details')});
 	} 	
}



cur_frm.cscript.refresh=function(doc,cdt,cdn){
	if(doc.docstatus == 1 && doc.stock_entry!=null) {
			cur_frm.add_custom_button(wn._('Generate Sample ID'),
			cur_frm.cscript['Creation Of Sample ID']);
	}

}

cur_frm.cscript['Creation Of Sample ID'] = function() {
	//alert("hi");
	wn.model.open_mapped_doc({
		method: "test.doctype.sample_entry.sample_entry.make_sample_id",
		source_name: cur_frm.doc.name
 	})

}


// make_sample_id= function() {
// 		wn.model.open_mapped_doc({
// 			method: "test.doctype.sam[ple_entry.sample_entry.make_sample_id",
// 			source_name: cur_frm.doc.name

// 		})
// }


// refresh: function(doc, dt, dn) {
//  		this._super(doc, dt, dn);
//  		if(doc.docstatus == 1 && doc.stock_entry!=null && doc.material_inward!=null) {