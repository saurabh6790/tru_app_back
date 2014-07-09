// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt





cur_frm.add_fetch('physical_condition_density', 'density_data','density_data');

cur_frm.add_fetch('physical_condition_density', 'temperature_data','temperature_data');

cur_frm.add_fetch('physical_condition_density', 'density','density');


cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}


cur_frm.cscript.validate=function(){

	refresh_field('density_mois')
	refresh_field('moisture')
}

cur_frm.fields_dict['physical_condition_density'].get_query=function(doc,cdt,cdn)
{
  return{
    query:"test.doctype.moisture_content.moisture_content.get_physical_density_details",
    filters:{
			"sample_no":doc.sample_no
		}
    
  }
}

// cur_frm.cscript.refresh=function(doc,cdt,cdn){
//   if(doc.docstatus == 1) {
//       cur_frm.add_custom_button(wn._('Calculate Neutralisation Value'),
//       cur_frm.cscript['Calculation Neutralisation Value']);

//     }

// }




// cur_frm.cscript['Calculation Neutralisation Value'] = function() {
//   //alert("hi");
//   wn.model.open_mapped_doc({
//     method: "test.doctype.moisture_content.moisture_content.calculate_neutralisation_value",
//     source_name: cur_frm.doc.name
//   })

// }