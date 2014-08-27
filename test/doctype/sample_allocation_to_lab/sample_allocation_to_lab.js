
// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.priority = function(doc,cdt,cdn){
  if (doc.priority){
  	//var cnt;
    get_server_fields('get_sample_details',doc.priority,'',doc,cdt,cdn,1,function(r,rt){refresh_field('prioritywise_sample_allocation')});
    refresh_field('flag1');
    refresh_field('flag2');
    refresh_field('flag3');

	}
  
}

cur_frm.cscript.refresh=function(doc,cdt,cdn){
  if(doc.docstatus == 1) {
      cur_frm.add_custom_button(wn._('Sample Allocation To Tester'),
      cur_frm.cscript['Sample Allocation To Tester']);

    }
}


cur_frm.cscript['Sample Allocation To Tester'] = function() {
  //alert("hi");
  wn.model.open_mapped_doc({
    method: "test.doctype.sample_allocation_to_lab.sample_allocation_to_lab.sample_allocation_to_tester",
    source_name: cur_frm.doc.name
  })

}


cur_frm.cscript.make_final_lab_entry = function(doc,cdt,cdn) {
	//console.log("yes");
	var cl = getchildren('Priority Wise Sample Allocation', doc.name, 'prioritywise_sample_allocation');
	//console.log(cl.length);

	if (cl.length>0 && doc.priority)

		get_server_fields('get_prioritywise_details','','',doc,cdt,cdn,1,function(r,rt){refresh_field('final_sample_allocation')});
	else
		msgprint("To Make Final Lab Entry Priority  & PriorityWise Sample Allocation Table details must be specified");

}

cur_frm.cscript.onload = function(doc,dt,dn){
	//console.log("samples allocation to lab");
	wn.call({
		method:"test.doctype.sample_allocation_to_lab.sample_allocation_to_lab.get_count",
		callback:function(r){
			//console.log(r.message);
			show_popup(doc,dt,dn,r.message)
		}
	})
	
}

var show_popup = function(doc,dt,dn,count){
	//console.log(count[0][1]);
	if(doc.docstatus!=1){
		var d = new wn.ui.Dialog({
		title:wn._('Get Total Samples'),
		fields: [

			{fieldtype:'HTML', fieldname:'critical_count',options:'<div id="count"></div>', label:wn._('Total Critical Samples'), reqd:false, 
				description: wn._("Total No. Of Critical Samples Available")},

			// {fieldtype:'Data', fieldname:'normal_count', label:wn._('Total Normal Samples'), reqd:true, 
			// 	description: wn._("Total No. Of  Normal Samples Available")},

			// {fieldtype:'Data', fieldname:'urgent_count', label:wn._('Total Urgent Samples'), reqd:true, 
			// 	description: wn._("Total No. Of  Urgent Samples Available")},

			{fieldtype:'Data', fieldname:'critical', label:wn._('Critical'), reqd:true, 
				description: wn._("No. Of Critical Samples Required")},

			{fieldtype:'Data', fieldname:'normal', label:wn._('Normal'), reqd:true, 
				description: wn._("No. Of Normal Samples Required")},
				
			{fieldtype:'Data', fieldname:'urgent', label:wn._('Urgent'), reqd:true, 
				description: wn._("No. Of Urgent Samples Required")},

			{fieldtype:'Button', fieldname:'done', label:wn._('Done') }
		]
	})
		
		$('#count').html("<b>Priority Wise Sample Count<br>"+ count[0][0] +" : " +count[0][1]+ "\
			<br>"+ count[1][0] + " : " + count[1][1]+"<br>"+count[2][0]+" : " + count[2][1])
		var fd = d.fields_dict;
		//console.log(fd);
		//console.log(fd[df['critical_count']]);
		$(fd.done.input).click(function() {
				var btn = this;
				$(btn).set_working();
				var values  = d.get_values();
				if(!values) return;
				//console.log(eval(values)['critical']);	
				doc.critical_samples=eval(values)['critical'];
				doc.normal_samples=eval(values)['normal'];
				doc.urgent_samples=eval(values)['urgent'];
				refresh_field('critical_samples');
				refresh_field('normal_samples');
				refresh_field('urgent_samples');
				$(btn).done_working();
				d.hide();
			});

		d.show();

	}
}