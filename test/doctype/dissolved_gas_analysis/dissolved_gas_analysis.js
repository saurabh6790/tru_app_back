// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}


cur_frm.cscript.run1= function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	if (d.gas=='TGS'){
		console.log(d.run1);
		doc.run=d.run1;
		refresh_field('run');
	}
	else{
		console.log("hi");
		return get_server_fields('get_dissolvedgas_details',d.run1, 'dissolved_gas_detail', doc, cdt, cdn, 1)

	}
		

}