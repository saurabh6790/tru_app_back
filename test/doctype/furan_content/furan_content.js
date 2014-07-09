// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.add = function(doc,cdt,cdn){
  console.log(doc.equipment_used);
  get_server_fields('add_equipment',doc.equipment_used,'',doc,cdt,cdn,1);
  refresh_field('equipment_used_list')
}


// cur_frm.cscript.onload = function(doc,dt,dn){
// 	//console.log("samples allocation to lab");
// 	if(!doc.sample_no){
// 		var d = new wn.ui.Dialog({
// 		title:wn._('Allocate Sample ID'),
// 		fields: [
		
// 			{fieldtype:'Link', fieldname:'sample_no', label:wn._('Sample No'), options:'Sample',reqd:true, 
// 				description: wn._("Sample No Allocation")},

// 			{fieldtype:'Button', fieldname:'add', label:wn._('ADD') }
// 		]
// 	})
// 		var fd = d.fields_dict;
// 		$(fd.add.input).click(function() {
// 				var btn = this;
// 				$(btn).set_working();
// 				var values  = d.get_values();
// 				if(!values) return;
// 				//console.log(eval(values)['critical']);	
// 				doc.sample_no=eval(values)['sample_no'];
// 				refresh_field('sample_no');
// 				$(btn).done_working();
// 				d.hide();
// 			});

//  		d.show();
// 	}
// 	}