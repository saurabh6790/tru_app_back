wn.pages['sample-generation'].onload = function(wrapper) { 
	wn.ui.make_app_page({
		parent: wrapper,
		title: 'Sample Generation',
		single_column: true
	});
	$(wrapper).find(".layout-main").html("<div class='user-settings'></div>\
	<table class='table table-bordered' style='background-color: #f9f9f9;'>\
	<tr><td>\
	<h4><i class='icon-question-sign'></i> "+wn._("Quick Help for Sample Entry Sorting and Sample Id Creation")+":</h4>\
	<ol>\
	<li>"+wn._("Data will be as per the filters you have selected")+"</li>\
	<li>"+wn._("To sort data click on downarrow icon")+"</li>\
	<li>"+wn._("For Getting a view click on eye icon")+"</li>\
	</ol>\
	</tr></td>\
	</table>");
	wrapper.user_properties = new wn.UserProperties(wrapper);			
}

wn.UserProperties = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".user-settings");
		this.make();
	},
	make: function() {
		var me = this;
		return wn.call({
			module:"test",
			page:"sample_generation",
			method: "get_tasnformer",
			callback: function(r) {
				me.options = r.message;
				me.from_date =
					me.wrapper.appframe.add_date("From Date", 
						'')
						.css("width", "200px")
						.change(function() {
							me.set_route();
						});
				me.transfromer =
					me.wrapper.appframe.add_select("Sample Id", 
						["Select Transformer..."].concat(r.message.transfromer_id))
						.css("width", "200px")
						.change(function() {
							me.set_route();
						});
				me.button=
					me.wrapper.appframe.add_button(wn._("Sort By"), function() {
							me.make_button()
						}, "icon-arrow-down").css("width", "50px")
				me.button1=
					me.wrapper.appframe.add_button(wn._("Display Results"), function() {
							me.get_result()
						}, "icon-eye-open").css("width", "50px")
			}
		});
	},
	make_button: function(){
		var me = this;
		var d = new wn.ui.Dialog({
			title: "Add New Property",
			fields: [
				{fieldtype:"Select", label:wn._("Sort By"),
					options:"\nFunctional Location\nPlant\nSub SStation", reqd:1, fieldname:"parent"},
				{fieldtype:"Select", label:wn._("Order"),
					options:"\nAscending\nDescending", reqd:1, fieldname:"parent1"},
				{fieldtype:"Select", label:wn._("Sort By"),
					options:"\nFunctional Location\nPlant\nSub SStation", reqd:1, fieldname:"parent2"},
				{fieldtype:"Select", label:wn._("Order"),
					options:"\nAscending\nDescending", fieldname:"parent3"},
				{fieldtype:"Button", label: wn._("Add"), fieldname:"add"},
			]
		});		
		d.get_input("add").click(function() {
			var args = d.get_values();
			if(!args) {
				return;
			}
			wn.call({
				module: "test",
				page: "sample_generation",
				method: "save_sorting_order",
				args: args,
				callback: function(r) {
				}
			})
			d.hide();
		});
		d.show();
	},
	get_result: function(){
		me = this;
		return wn.call({
			module:"test",
			page:"sample_generation",
			method: "get_sample_entries",
			args:{'date': this.from_date.val(), 'transfromer': this.transfromer.val()},
			callback: function(r) {
				console.log(r.message.sample_entry.length)
				if(r.message.sample_entry.length <= 0){
					msgprint(wn._("Sample Id is created for all Sample Entries"))
				}
				else{
					me.options = r.message;
					me.show_sample_entry(r.message.sample_entry)
					me.button1=
						me.wrapper.appframe.add_button(wn._("Create Sample"), function() {
							me.sample_creation()
						}, "icon-cogs").css("width", "50px")
						me.wrapper.appframe.add_button(wn._('Chart of Cost Centers'), function() { 
							wn.set_route("Form","Test Allocation Interface", "Test Allocation Interface"); 
						}, 'icon-sitemap').css("width", "50px")
				}
									
			}
		});
	},
	show_sample_entry: function(sample_entry){
		this.body.empty();
		var me = this;
		columns = [[wn._("Sample Entry"), 50], [wn._("Plant"), 50], [wn._("Functional Location"),50], [wn._("Sub Station"), 50], [wn._("Rating"),50]];

		if(sample_entry[0].sample_id){
			columns.push([wn._('Sample Id'),50])
		}
		else{
			columns.push(['',50])
		}

		this.table = $("<table class='table table-bordered'>\
			<thead><tr></tr></thead>\
			<tbody></tbody>\
		</table>").appendTo(this.body);
		
		$.each(columns, 
			function(i, col) {
			$("<th>").html(col[0]).css("width", col[1]+"px")
				.appendTo(me.table.find("thead tr"));
		});

				
		$.each(sample_entry, function(i, d) {
			var row = $("<tr>").appendTo(me.table.find("tbody"));
			
			$("<td>").html('<a href="#Form/Sample Entry/'+d.name+'">'
				+d.name+'</a>').appendTo(row);
			$("<td>").html(d.functional_location).appendTo(row);
			$("<td>").html(d.plant).appendTo(row);
			$("<td>").html(d.sub_station).appendTo(row);
			$("<td>").html(d.rating).appendTo(row);
			if(d.sample_id){
				$("<td>").html(d.sample_id).appendTo(row);
			}
			else{
				me.add_delete_button(row, d);
			}
		});
	},
	add_delete_button: function(row, d) {
		var me = this;
		$("<button class='btn btn-small btn-default'><i class='icon-trash'></i></button>")
			.appendTo($("<td>").appendTo(row))
			.attr("data-name", d.name)
			.click(function() {
				me.remove_sample_entry($(this).attr("data-name"))
			});
	},
	remove_sample_entry: function(sample_entry_id) {
		var counter = 0;
		for(dict in this.options.sample_entry){
			counter = counter + 1;
			if(this.options.sample_entry[dict]['name'] == sample_entry_id){
				this.options.sample_entry.splice(counter-1,1);
				me.show_sample_entry(this.options.sample_entry);
				break;
			}
		}
	},
	sample_creation: function(){
		me = this;
		console.log(this.options)
		return wn.call({
			module:"test",
			page:"sample_generation",
			method: "sample_generation",
			args:{'sample_entries':this.options.sample_entry},
			callback: function(r) {
				me.show_sample_entry(r.message.sample_entries)					
			}
		});
	},
	set_route: function() {
		console.log(this.from_date.val())
	}
})