

cur_frm.cscript.get_details=function(doc,cdt,cdn){
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

	mapper['Test Of Extract Test Details'] = {}
	mapper['Test Of Extract Test Details']['name'] = 'sediment_test_id';

	mapper['Kinematic Viscocity Test Details'] = {}
	mapper['Kinematic Viscocity Test Details']['name'] = 'kinematic_viscosity_test_id';

	mapper['Pour Point Test Details'] = {}
	mapper['Pour Point Test Details']['name'] = 'pour_point_test_id';

	mapper['Dissolved Gas Analysis Test Details'] = {}
	mapper['Dissolved Gas Analysis Test Details']['name'] = 'dissolved_gas_test_id';

	mapper['Furan Content Test Details'] = {}
	mapper['Furan Content Test Details']['name'] = 'furan_content_test_id';
	
	mapper['PCB Test Details'] = {}
	mapper['PCB Test Details']['name'] = 'pcb_test_id';
	
	mapper['Corrosive Sulphur Test Details'] = {}
	mapper['Corrosive Sulphur Test Details']['name'] = 'corrosive_sulphur_test_id';

	mapper['Oxidation Inhibiters Test Details'] = {}
	mapper['Oxidation Inhibiters Test Details']['name'] = 'oxidation_inhibiters_test_id';
	
	mapper['Metal In Oil Test Details'] = {}
	mapper['Metal In Oil Test Details']['name'] = 'metal_in_oil_test_id';
	
	mapper['Interfacial Tension Test Details'] = {}
	mapper['Interfacial Tension Test Details']['name'] = 'ift_test_id';

	// mapper['Interfacial Tension Test Details']['name'] = 'ift_test_id';
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