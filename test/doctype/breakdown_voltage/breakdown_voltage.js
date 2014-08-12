// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.cscript.validate=function(doc,cdt,cdn){
	console.log(this)
	refresh_field(['break_down_temperature','break_down_humidity','break_down_ir','break_down_frequency'])
}

cur_frm.cscript.add = function(doc,cdt,cdn){

	get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
	refresh_field('equipment_used_list')
}
