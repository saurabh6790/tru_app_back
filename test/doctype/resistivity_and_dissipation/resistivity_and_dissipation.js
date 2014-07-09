// cur_frm.cscript.sample_no=function(doc,cdt,cdn){
// 	get_server_fields('get_barcode',doc.sample_no,'',doc,cdt,cdn,1)
// 	refresh_field('bottle_no')
// }

cur_frm.cscript.validate=function(doc,cdt,cdn){
	refresh_field('tan_value')
	refresh_field('sigma_value')
	refresh_field('resistivity_value')
}

cur_frm.cscript.add = function(doc,cdt,cdn){
	get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
	refresh_field('equipment_used_list')
}

cur_frm.cscript.calculate = function(doc, dt, dn){
	var d = locals[dt][dn]
	d.tan_value = ((parseFloat(d.frequency)/parseFloat(d.reported_hz))*(parseFloat(d.ir_tan)*parseFloat(d.power_tan))).toFixed(6)
	refresh_field('tan_value', d.name, 'tan_details');
}

cur_frm.cscript.ir = function(doc, dt, dn){
	doc.sigma_value = 2+parseFloat(doc.ir)/1000;
	refresh_field('sigma_value')
}

cur_frm.cscript.power_resistivity = function(doc, dt, dn){
	var d = locals[dt][dn];
	var power = d.power_resistivity.split('^')[1];
	var final_power = parseInt(power)-(12)
	d.resistivity_value = parseFloat(d.ir_resistivity)*10^final_power;
	refresh_field('resistivity_value', d.name, 'resistivity_details');
}

cur_frm.cscript.test_temperature = function(doc, dt, dn){
	var d = locals[dt][dn];
	d.sample_no = doc.sample_no;
	refresh_field('sample_no', d.name, 'tan_details');
}

cur_frm.cscript.temperature = function(doc, dt, dn){
	var d = locals[dt][dn];
	d.sample_no = doc.sample_no;
	refresh_field('sample_no', d.name, 'resistivity_details');
}
cur_frm.cscript.refresh=function(doc,cdt,cdn){
  if(doc.docstatus == 1 && doc.test=='Accelerated Aging') {
      cur_frm.add_custom_button(wn._('Calculate Neutralisation Value'),
      cur_frm.cscript['Calculate Neutralisation value']);

    }
}

cur_frm.cscript['Calculate Neutralisation value'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.resistivity_and_dissipation.resistivity_and_dissipation.calculate_neutralization_value",
    source_name: cur_frm.doc.name
  })

}



cur_frm.fields_dict['sample_no'].get_query=function(doc,cdt,cdn)
{
	if(doc.test_preparation && doc.test){
  		return{
    		query:"test.doctype.resistivity_and_dissipation.resistivity_and_dissipation.get_sample_no",
    		filters:{
				"test_preparation":doc.test_preparation,
				"test":doc.test
			}
    
  		}
	}
}
// cur_frm.cscript.onload = function(doc,dt,dn){
// 	//console.log("samples allocation to lab");
// 	if(doc.test=='Accelerated Aging' && !doc.sample_no){
// 		var d = new wn.ui.Dialog({
// 		title:wn._('Allocate Sample ID'),
// 		fields: [
		
// 			{fieldtype:'Link', fieldname:'sample_no', label:wn._('Sample No'), options:'Sample',reqd:true, 
// 				description: wn._("Sample No Allocation")},

// 			{fieldtype:'Button', fieldname:'add', label:wn._('ADD') }
// 		]
// 	})
// 		var fd = d.fields_dict;
// 		$(fd.add.input).click(function() {
// 				var btn = this;
// 				$(btn).set_working();
// 				var values  = d.get_values();
// 				if(!values) return;
// 				//console.log(eval(values)['critical']);	
// 				doc.sample_no=eval(values)['sample_no'];
// 				refresh_field('sample_no');
// 				$(btn).done_working();
// 				d.hide();
// 			});

//  		d.show();
//  	}
// 	}