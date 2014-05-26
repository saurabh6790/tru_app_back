cur_frm.cscript.sample_no=function(doc,cdt,cdn){
	get_server_fields('get_details','','',doc,cdt,cdn,1,function(r){
		cur_frm.cscript.set_values(r.results, doc, cdt, cdn)
	})
}

cur_frm.cscript.set_values = function(result, doc, cdt, cdn){
	var mapper = {};

	mapper['Physical Condition And Density'] = {};
	mapper['Physical Condition And Density']['name'] = 'pcd_test_id';
	mapper['Moisture Content'] = {};
	mapper['Moisture Content']['name'] = 'moisture_test_id';
	mapper['Resistivity and Dissipation'] = {};
	mapper['Resistivity and Dissipation']['name'] = 'rd_test_id';
	mapper['Breakdown Voltage'] = {};
	mapper['Breakdown Voltage']['name'] = 'bv_test_id';
	mapper['Flash Point'] = {};
	mapper['Flash Point']['name'] = 'bv_test_id';
	mapper['Neutralization Test Details'] = {};
	mapper['Neutralization Test Details']['parent'] = 'neutralization_test_id';
	// mapper['Neutralization Test Details']['neutralization_test_details'] = 'neutralization_value';


	// console.log(mapper)
	for(r in result){
		for(param in result[r][0]){
			var param1 = param;
			if(param == 'name'){
				param = mapper[r]['name']
			}
			if(param == 'parent'){
				param = mapper[r]['parent']	
			}
			cur_frm.set_value(param, result[r][0][param1])
			refresh_field(param)
		}
		if(r=='Neutralization Test Details'){
			r='neutralization_value'
		}
		unhide_field(r.toLowerCase().replace(/ /g, '_'))
	}

}