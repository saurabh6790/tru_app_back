
// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

cur_frm.add_fetch('equipment_id', 'serial_no','serial_no');

cur_frm.add_fetch('equipment_id', 'make','make');

cur_frm.add_fetch('equipment_id', 'phase','phase');

cur_frm.add_fetch('equipment_id', 'year_of_mfg','year_of_mfg');

cur_frm.add_fetch('equipment_id', 'voltage_ratio','voltage_ratio');

cur_frm.add_fetch('equipment_id', 'rating','rating');

cur_frm.add_fetch('equipment_id', 'ratio','ratio');






cur_frm.cscript.attach_dettach = function(doc,cdt,cdn) {
	if (doc.equipment_id){
		args={
    			"equipment_id":doc.equipment_id,
    			"plant":doc.plant,
          "sub station":doc.sub_station,
          "functional_location":doc.functional_location,
    			"client":doc.client_name
    	}
    	//msgprint(args);
	}
	return 	get_server_fields('get_new_equipmentid',JSON.stringify(args),'',doc,cdt,cdn,1);//,function(r,rt){refresh_field('training')});

}


// cur_frm.cscript.equipment_id = function(doc,cdt,cdn){
//   if (doc.equipment_id)

//     return get_server_fields('get_equipmentid_record',doc.equipment_id,'',doc,cdt.cdn,1);
  
// }

cur_frm.cscript.refresh = function(doc, dt, dn) {
	if(doc.__islocal){
		hide_field('attach_dettach'); 
    
	}
  	else{
    	unhide_field('attach_dettach');
  	}
}