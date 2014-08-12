// // Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// // License: GNU General Public License v3. See license.txt



cur_frm.cscript.weight_of_syringe = function(doc, cdt, cdn) {
   var d = locals[cdt][cdn];
   //console.log(d.weight_of_syringe);
    
    	//console.log("insiede");
    	//args={}
    	args={
    		"temp":d.temparature,
    		"weight":d.weight_of_empty_syringe,
    		"volume":d.volume_of_oil,
    		"syringe":d.weight_of_syringe
    	}
    	
    //console.log(args);
       return get_server_fields('get_density_details',JSON.stringify(args), 'density_details', doc, cdt, cdn, 1)
}

cur_frm.cscript.temparature = function(doc,cdt,cdn){
  cur_frm.cscript.weight_of_syringe(doc,cdt,cdn)
}

cur_frm.cscript.weight_of_empty_syringe = function(doc,cdt,cdn){
  cur_frm.cscript.weight_of_syringe(doc,cdt,cdn)
}

cur_frm.cscript.volume_of_oil = function(doc,cdt,cdn){
  cur_frm.cscript.weight_of_syringe(doc,cdt,cdn)
}

// cur_frm.cscript.refresh=function(doc,cdt,cdn){
//   if(doc.docstatus == 1) {
//       cur_frm.add_custom_button(wn._('Calculate Moisture Content'),
//       cur_frm.cscript['Calculation Moisture Content']);

//       cur_frm.add_custom_button(wn._('Calculate Interfacial Tension'),
//       cur_frm.cscript['Calculate Interfacial Tension']);


//       cur_frm.add_custom_button(wn._('Calculate Neutralisation Value'),
//       cur_frm.cscript['Calculation Neutralisation Value']);

//   }

// }

// cur_frm.cscript.sample_no=function(doc,cdt,cdn){
//   get_server_fields('get_barcode',doc.sample_no,'',doc,cdt,cdn,1)
//   refresh_field('bottle_no')
// }



// cur_frm.cscript['Calculation Moisture Content'] = function() {
//   //alert("hi");
//   wn.model.open_mapped_doc({
//     method: "test.doctype.physical_condition_and_density.physical_condition_and_density.calculate_moisture_content",
//     source_name: cur_frm.doc.name
//   })

// }


// cur_frm.cscript['Calculate Interfacial Tension'] = function() {
//   //alert("hi");
//   wn.model.open_mapped_doc({
//     method: "test.doctype.physical_condition_and_density.physical_condition_and_density.calculate_interfacial_tension",
//     source_name: cur_frm.doc.name
//   })

// }



// cur_frm.cscript['Calculation Neutralisation Value'] = function() {
//   //alert("hi");
//   wn.model.open_mapped_doc({
//     method: "test.doctype.physical_condition_and_density.physical_condition_and_density.calculate_neutralisation_value",
//     source_name: cur_frm.doc.name
//   })

// }



cur_frm.cscript.add = function(doc,cdt,cdn){
  console.log(doc.equipment_used);
  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}
