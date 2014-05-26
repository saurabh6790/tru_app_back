// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt



// cur_frm.cscript.refresh = function(doc,cdt,cdn){
// 	console.log(doc.workflow_state);
// 	var cl = getchildren('Break Details', doc.name, 'break_detail');
// 	console.log(cl);
// 	// if(cl.length>=6)
// 	// 	console.log("OK");
// 	// else
// 	// 	msgprint("Minimum six record needed for break details");
// }

cur_frm.cscript.sample_no=function(doc,cdt,cdn){
  get_server_fields('get_barcode',doc.sample_no,'',doc,cdt,cdn,1)
  refresh_field('bottle_no')
}

cur_frm.cscript.validate=function(doc,cdt,cdn){
	refresh_field(['break_down_temperature','break_down_humidity','break_down_ir','break_down_frequency'])
}