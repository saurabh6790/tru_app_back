// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}



cur_frm.cscript.refresh=function(doc,cdt,cdn){
  if(doc.docstatus == 1) {
      cur_frm.add_custom_button(wn._('Calculate Testing Of Extract'),
      cur_frm.cscript['Calculate Testing Of Extract']);

    }
}




cur_frm.cscript['Calculate Testing Of Extract'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.sediment.sediment.calculate_testing_of_extract",
    source_name: cur_frm.doc.name
  })

}