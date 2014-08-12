// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



cur_frm.add_fetch('physical_condition_density', 'density_data','density_data');

cur_frm.add_fetch('physical_condition_density', 'temperature_data','temperature_data');

cur_frm.add_fetch('physical_condition_density', 'density','density');

cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}



cur_frm.cscript.normality=function(doc, cdt, cdn){
	get_server_fields('retrieve_normality_values','','',doc,cdt,cdn,1,function(){
		refresh_field(['normality_of_hcl','volume','koh_volume','normality_of_koh','method'])
	})
}


cur_frm.cscript.temperature_of_oil= function(doc, cdt, cdn) {
   var d = locals[cdt][cdn];
   if(d.temperature_of_oil && d.physical_condition_density){
    args={
      
        "temp":d.temperature_of_oil,
        "temperature_data":d.temperature_data,
        "density":d.density_data
      }

   	return get_server_fields('get_density_details',JSON.stringify(args), 'neutralisation_test_details', doc, cdt, cdn, 1)
  }
}


cur_frm.cscript.ml_consumes_of_alkoh= function(doc, cdt, cdn) {
   var d = locals[cdt][cdn];
   if(d.ml_consumes_of_alkoh && d.volume_of_oil && d.temperature_of_oil && doc.normality_of_koh){
   	if(d.ml_consumes_of_alkoh){
   	args={
    		//"temp":d.temparature,
    		"alkoh":d.ml_consumes_of_alkoh,
    		"temp":d.temperature_of_oil,
    		"volume":d.volume_of_oil,
    		"density":d.density_of_oil
    	}

   	return get_server_fields('get_neutralisation_details',JSON.stringify(args), 'neutralisation_test_details', doc, cdt, cdn, 1)
   }
	}
   else
   	msgprint("To calculate Neutralisation Value all the mandatory fields from main form & from child table must be filled");
}


cur_frm.get_field("normality").get_query=function(doc,cdt,cdn){

  return "select name from `tabNormality` order by creation desc" 

}
//cur_frm.fields_dict['neutralisation_test_details'].grid.get_field("physical_condition_density").get_query



cur_frm.fields_dict.neutralisation_test_details.grid.get_field("physical_condition_density").get_query = function(doc,cdt,cdn)
{
  var d = locals[cdt][cdn];
  if (d.sample_no)
    return "select name from `tabPhysical Condition And Density` where sample_no='"+d.sample_no+"' and docstatus=1"  
  else
    msgprint("Sample Number field for selecting physical condition & density");
}
// cur_frm.fields_dict['sample_no'].get_query=function(doc,cdt,cdn)
// { 
//   return{
//     query:"test.doctype.neutralization_value.neutralization_value.get_sample_details",
//     filters:{
//       "test_preparation":doc.test_preparation
//     }
    
//   }
// }
cur_frm.fields_dict['physical_condition_density'].get_query=function(doc,cdt,cdn)
{
  return{
    query:"test.doctype.neutralization_value.neutralization_value.get_physical_density_details",
    filters:{
      "sample_no":doc.sample_no
    }
    
  }
}


cur_frm.cscript.refresh=function(doc,cdt,cdn){
  if(doc.docstatus == 1 && (doc.test=='Accelerated Aging'|| doc.test=='Oxidation Stability')){
      cur_frm.add_custom_button(wn._('Prepare Sample For Sediment'),
      cur_frm.cscript['Prepare Sample For Sediment']);
    }

  // else if(doc.docstatus == 1 && doc.test=='Oxidation Stability') {
  //     cur_frm.add_custom_button(wn._('Prepare Sample For Sediment'),
  //     cur_frm.cscript['Prepare Sample For Sediment']);
  //   }
}


cur_frm.cscript['Prepare Sample For Sediment'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.neutralization_value.neutralization_value.prepare_sample_for_sediment",
    source_name: cur_frm.doc.name
  })

}

// cur_frm.cscript.onload = function(doc,dt,dn){
//   //console.log("samples allocation to lab");
//   var d = new wn.ui.Dialog({
//   title:wn._('Create New Normality/Select Normality'),
//   fields: [
    
//     {fieldtype:'Link', fieldname:'normality', label:wn._('Normality'), options:'Normality',reqd:true, 
//       description: wn._("Normality Test")},

//     {fieldtype:'Button', fieldname:'add', label:wn._('ADD') }
//   ]
// })
//   var fd = d.fields_dict;
//   $(fd.add.input).click(function() {
//       var btn = this;
//       $(btn).set_working();
//       var values  = d.get_values();
//       if(!values) return;
//       //console.log(eval(values)['critical']);  
//       doc.normality=eval(values)['normality'];
//       refresh_field('normality');
//       $(btn).done_working();
//       d.hide();
//     });

//   d.show();

// }
