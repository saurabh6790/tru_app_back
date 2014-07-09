// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



cur_frm.cscript.refresh=function(doc,cdt,cdn){
  if(doc.docstatus == 1 && doc.test=='Sediment') {
      cur_frm.add_custom_button(wn._('Calculate Testing Of Extract'),
      cur_frm.cscript['Calculate Testing Of Extract']);
   }

  else if(doc.docstatus == 1 && doc.test=='Furan Content') {
      cur_frm.add_custom_button(wn._('Calculate Furan Content'),
      cur_frm.cscript['Calculate Furan Content']);
   }
   else if(doc.docstatus == 1 && doc.test== 'Oxidation Stability'){
      
      cur_frm.add_custom_button(wn._('Calculate Neutralization Value'),
      cur_frm.cscript['Calculate Neutralization Value']);

      cur_frm.add_custom_button(wn._('Prepare Sample For Sediment'),
      cur_frm.cscript['Prepare Sample For Sediment']);

      
    }
   else if(doc.docstatus == 1 && doc.test== 'Corrossive Sulphur'){
   	  //alert("hi");
      cur_frm.add_custom_button(wn._('Calculate Corrosive Sulphur'),
      cur_frm.cscript['Calculate Corrosive Sulphur']);
    
   }
   else if(doc.docstatus == 1 && doc.test=='Accelerated Aging'){

      cur_frm.add_custom_button(wn._('Calculate Ressistivity And Dissipiation'),
      cur_frm.cscript['Calculate Ressistivity And Dissipiation']);

      cur_frm.add_custom_button(wn._('Calculate Neutralization Value'),
      cur_frm.cscript['Calculate Neutralization Value']);

      cur_frm.add_custom_button(wn._('Prepare Sample For Sediment'),
      cur_frm.cscript['Prepare Sample For Sediment']);

   }

    
}


cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}



// cur_frm.cscript.test = function(doc,cdt,cdn){
// 	if(doc.docstatus == 0 && doc.test== 'Oxidation Stability'){
// 		//console.log("hi");

// 		cur_frm.add_custom_button(wn._('Prepare Sample For Sediment'),
//       	cur_frm.cscript['Prepare Sample For Sediment']);

//       	cur_frm.add_custom_button(wn._('Calculate Neutralization Value'),
//       	cur_frm.cscript['Calculate Neutralization Value']);

// 	}
// }


cur_frm.cscript['Calculate Testing Of Extract'] = function() {

  wn.model.open_mapped_doc({
    method: "test.doctype.test_preparation.test_preparation.calculate_testing_of_extract",
    source_name: cur_frm.doc.name
  })

}


cur_frm.cscript['Calculate Furan Content'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.test_preparation.test_preparation.calculate_furan_content",
    source_name: cur_frm.doc.name
  })

}

cur_frm.cscript['Calculate Neutralization Value'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.test_preparation.test_preparation.calculate_neutralization_value",
    source_name: cur_frm.doc.name
  })

}

cur_frm.cscript['Prepare Sample For Sediment'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.test_preparation.test_preparation.prepare_sample_for_sediment",
    source_name: cur_frm.doc.name
  })

}


cur_frm.cscript['Calculate Corrosive Sulphur'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.test_preparation.test_preparation.calculate_corrosive_sulphur",
    source_name: cur_frm.doc.name
  })

}


cur_frm.cscript['Calculate Ressistivity And Dissipiation'] = function() {
  alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.test_preparation.test_preparation.calculate_ressistivity_and_dissipiation",
    source_name: cur_frm.doc.name
  })

}


