// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



// cur_frm.cscript.sample_no=function(doc,cdt,cdn){
//   get_server_fields('get_barcode',doc.sample_no,'',doc,cdt,cdn,1)
//   refresh_field('bottle_no')
// }


cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}
