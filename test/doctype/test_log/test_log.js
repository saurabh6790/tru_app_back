wn.TestLog = Class.extend({
	init:function(){
		this.make_popup()
	},
	make_popup: function(){
		var d = new wn.ui.Dialog({
			title:wn._('Get Total Samples'),
			fields: [
				{fieldtype:'Select', fieldname:'critical', label:wn._('Critical'), reqd:true, 
					options:"Accept\nReject", description: wn._("")},
				{fieldtype:'Button', fieldname:'done', label:wn._('Done') }
			]
		})
		var fd = d.fields_dict;
		$(fd.done.input).click(function() {
			var btn = this;
			$(btn).set_working();
			var values  = d.get_values();
			if(!values) return;
			//console.log(eval(values)['critical']);	
			
			$(btn).done_working();
			d.hide();
		});
		d.show();
	}
})