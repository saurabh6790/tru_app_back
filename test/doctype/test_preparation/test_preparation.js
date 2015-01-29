// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



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


cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}