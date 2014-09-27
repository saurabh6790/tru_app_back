// // Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// // License: GNU General Public License v3. See license.txt



cur_frm.add_fetch('physical_condition_density', 'density_data','density_data');

cur_frm.add_fetch('physical_condition_density', 'temperature_data','temperature_data');

cur_frm.add_fetch('physical_condition_density', 'density','density');

cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}



cur_frm.cscript.normality=function(doc, cdt, cdn){
	get_server_fields('retrieve_normality_values','','',doc,cdt,cdn,1,function(){
		refresh_field(['normality_of_hcl','volume','koh_volume','normality_of_koh','method'])
	})
}


cur_frm.cscript.temperature_of_oil= function(doc, cdt, cdn) {
  calculate_result(doc,cdt,cdn)

}

cur_frm.cscript.volume_of_oil= function(doc, cdt, cdn) {
  calculate_result(doc,cdt,cdn)

}
  

cur_frm.cscript.ml_consumes_of_alkoh= function(doc, cdt, cdn) {
  var d = locals[cdt][cdn];
   if(d.ml_consumes_of_alkoh && d.volume_of_oil && d.temperature_of_oil && doc.normality_of_koh){
          calculate_result(doc,cdt,cdn)


	}
   else
   	  msgprint("To calculate Neutralisation Value all the mandatory fields from main form & from child table must be filled");
}




cur_frm.get_field("normality").get_query=function(doc,cdt,cdn){

  return "select name from `tabNormality` order by creation desc" 

}


cur_frm.cscript.onload = function(doc, cdt, cdn){
  //logic to check open session
  check_session(doc,cdt,cdn)
}

check_session = function(doc,cdt,cdn){
  wn.call({
    method:"test.doctype.neutralization_value.neutralization_value.check_session",
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
    method:"test.doctype.neutralization_value.neutralization_value.create_session",
    callback:function(r){
      cur_frm.set_value('session_id',r.message.session_id)
      refresh_field('session_id')
      hide_field('start_session');
      unhide_field('end_session');
    }
  })
}


cur_frm.cscript.physical_condition_density=function(doc,cdt,cdn){
    var d = locals[cdt][cdn];
    get_server_fields('get_physical_density_details',d.sample_no,'',doc,cdt,cdn,1);

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


calculate_result =function(doc,cdt,cdn){
  //console.log("in calculate result")
  var d = locals[cdt][cdn];
  if(d.physical_condition_density){
    cal=((1)+(0.00065*(d.temperature_data-d.temperature_of_oil)))
    density= (d.density_data*cal)
    //console.log(density);
    d.density_of_oil=density
    refresh_field('density_of_oil',d.name,'neutralisation_test_details')
    cal1=(56.1*(d.ml_consumes_of_alkoh* doc.normality_of_koh))
    //console.log(cal1);
    neutralisation=(cal1/(d.density_of_oil*d.volume_of_oil))
    //console.log(neutralisation);
    d.reported_value= neutralisation
    refresh_field('reported_value',d.name,'neutralisation_test_details')

  }
}

cur_frm.cscript.refresh=function(doc,cdt,cdn){
  if(doc.docstatus == 1 && (doc.test=='Accelerated Aging'|| doc.test=='Oxidation Stability')){
      cur_frm.add_custom_button(wn._('Prepare Sample For Sediment'),
      cur_frm.cscript['Prepare Sample For Sediment']);
    }

  else if(doc.docstatus == 1 && doc.test=='Oxidation Stability') {
      cur_frm.add_custom_button(wn._('Prepare Sample For Sediment'),
      cur_frm.cscript['Prepare Sample For Sediment']);
    }
}


cur_frm.cscript['Prepare Sample For Sediment'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.neutralization_value.neutralization_value.prepare_sample_for_sediment",
    source_name: cur_frm.doc.name
  })

}

