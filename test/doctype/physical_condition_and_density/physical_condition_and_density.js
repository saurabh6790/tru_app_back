// // Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// // License: GNU General Public License v3. See license.txt



cur_frm.cscript.weight_of_syringe = function(doc, cdt, cdn) {
   var d = locals[cdt][cdn];
   
      if(d.temparature && d.weight_of_empty_syringe && d.volume_of_oil && d.weight_of_syringe){
      	args={
      		"temp":d.temparature,
      		"weight":d.weight_of_empty_syringe,
      		"volume":d.volume_of_oil,
      		"syringe":d.weight_of_syringe
      	}
        return get_server_fields('get_density_details',JSON.stringify(args), 'density_details', doc, cdt, cdn, 1)
    	}
    //console.log(args);
       
}
cur_frm.cscript.temparature = function(doc, cdt, cdn){
  cur_frm.cscript.weight_of_syringe(doc, cdt, cdn)
}

cur_frm.cscript.weight_of_empty_syringe = function(doc, cdt, cdn){
  cur_frm.cscript.weight_of_syringe(doc, cdt, cdn)
}

cur_frm.cscript.volume_of_oil = function(doc, cdt, cdn){
  cur_frm.cscript.weight_of_syringe(doc, cdt, cdn)
}




cur_frm.cscript.add = function(doc,cdt,cdn){
  console.log(doc.equipment_used);
  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}
