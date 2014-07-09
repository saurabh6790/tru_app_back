// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.add_fetch('physical_condition_density', 'density_data','density_data');

cur_frm.add_fetch('physical_condition_density', 'temperature_data','temperature_data');

cur_frm.add_fetch('physical_condition_density', 'density','density');


cur_frm.cscript.validate=function(doc, cdt, cdn){
	refresh_field('density_of_oil')
}

cur_frm.cscript.ir = function(doc, cdt, cdn){
	get_server_fields('calculate_density','','',doc,cdt,cdn,1, function(r){
		// console.log(r)
		cur_frm.set_value('density_of_oil_reported_temp',r.density_of_oil)
		refresh_field('density_of_oil_reported_temp')
	});
}

cur_frm.cscript.calculate_ift = function(doc, cdt, cdn){
	get_server_fields('calc_ift','','',doc,cdt,cdn,1, function(r){
		// console.log(r)
		cur_frm.set_value('ift',r.ift)
		refresh_field('ift')
	});
}

cur_frm.cscript.onload = function(doc, cdt, cdn){
	//logic to check open session
	check_session(doc,cdt,cdn)
}

check_session = function(doc,cdt,cdn){
	wn.call({
		method:"test.doctype.interfacial_tension.interfacial_tension.check_session",
		callback:function(r){
			if(r.message.session_id){
				cur_frm.set_value('session_id',r.message.session_id)
				refresh_field('session_id')
				hide_field('start_session');
				unhide_field('end_session');
			}
			else{
				cur_frm.set_value('session_id',r.message.session_id)
				refresh_field('session_id')
				unhide_field('start_session');
				hide_field('end_session');
			}
		}
	})
}

cur_frm.cscript.start_session = function(doc, cdt, cdn){
	//create new session
	wn.call({
		method:"test.doctype.interfacial_tension.interfacial_tension.create_session",
		callback:function(r){
			cur_frm.set_value('session_id',r.message.session_id)
			refresh_field('session_id')
			hide_field('start_session');
			unhide_field('end_session');
		}
	})
}

cur_frm.cscript.end_session = function(doc, cdt, cdn){
	//close the current session

	wn.call({
		method:"test.doctype.interfacial_tension.interfacial_tension.close_session",
		args:{
			'session_id':doc.session_id
		},
		callback:function(r){
			cur_frm.set_value('session_id',r.message.session_id)
			refresh_field('session_id')
			unhide_field('start_session');
			hide_field('end_session');
		}
	})
}

cur_frm.cscript.add = function(doc,cdt,cdn){

	get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
	refresh_field('equipment_used_list')
}


cur_frm.fields_dict['physical_condition_density'].get_query=function(doc,cdt,cdn)
{
  return{
    query:"test.doctype.moisture_content.moisture_content.get_physical_density_details",
    filters:{
			"sample_no":doc.sample_no
		}
    
  }
}