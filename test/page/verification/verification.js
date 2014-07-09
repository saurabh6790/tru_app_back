wn.pages['verification'].onload = function(wrapper) { 
	wn.ui.make_app_page({
		parent: wrapper,
		title: 'Verification',
		single_column: true
	});	
	$(wrapper).find(".layout-main").html("<div class='user-settings'></div>\
	<table class='table table-condensed'>\
	<tr><td colspan='2'><div id= 'test_cerficate'></div></td></tr>\
	<tr><td style='width:30%;'><div id= 'test'></div></td>\
	<td style='width:70%;'><div id= 'test_results'></td></tr>\
	</table>");
	wrapper.test_details = new wn.TestDetails(wrapper);
	wrapper.notification = new wn.Notification(wrapper);
	setInterval(function(){wrapper.notification = new wn.Notification(wrapper);}, 60000);
				
}

wn.TestDetails = Class.extend({
	init: function(wrapper) {
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".user-settings");
		this.make();
	},
	make:function(){
		var me = this;
		wn.call({
			method: "test.page.verification.verification.roles",
			callback: function(r){
				console.log(r.message.roles)
				if(r.message.roles[0] == 'Lab Incharge' || r.message.roles[0] == 'Administrator'){me.setup_filters()}
				me.render_tests()
			}
		})
	},
	setup_filters: function(){
		var me = this;
		return wn.call({
			method: "test.page.verification.verification.get_tasnformer",
			args:{
				'test_names':get_test_list()
			},
			callback: function(r) {
				me.options = r.message;
				me.transfromer =
					me.wrapper.appframe.add_select("Transformer", 
						["Select Transformer..."].concat(r.message.transfromer_id))
						.css("width", "200px")
						.change(function() {
							me.show_certificates()
						});
			}
		});
	},
	show_certificates: function(){
		var me = this;
		wn.call({
			method:"test.page.verification.verification.get_certi",
			args:{"transfromer":this.transfromer.val()},
			callback: function(r){
				me.render_certi(r.message.certi)
			}
		})
	},
	render_certi: function(certi){
		console.log(certi)
		var me = this;
		this.test_names = $(this.wrapper).find('#test_cerficate');
		test_list = get_test_list();

		this.table = $("<table class='table table-bordered'>\
			<thead><tr></tr></thead>\
			<tbody></tbody>\
		</table>").appendTo(this.test_names);

		columns = [[wn._("Certificates"), 50]]

		$.each(columns, 
			function(i, col) {
			$("<th>").html(col[0]).css("width", col[1]+"px")
				.appendTo(me.table.find("thead tr"));
		});

		$.each(certi, 
			function(i, d) {
			var row = $("<tr id="+i+">").appendTo(me.table.find("tbody"));
			$("<td>").html('<a href="#Form/Test Certificate/'+d[0]+'">'
				+d[0]+'</a>').appendTo(row);
		});
	},
	render_tests: function(){
		var me = this;
		this.test_names = $(this.wrapper).find('#test');
		test_list = get_test_list();

		this.table = $("<table id='test_name_list' class='table table-bordered'>\
			<thead><tr></tr></thead>\
			<tbody></tbody>\
		</table>").appendTo(this.test_names);

		$.each(test_list, 
			function(i, test) {
			var row = $("<tr id="+i+">").appendTo(me.table.find("tbody"));
			$("<td>").html(test+'<span id='+test.replace(/[ ]/g,'_')+' \
			style ="display:inline-block;margin-left:10px;color:white;text-align:center;width:20px;background-color:#FF5252;border-radius: 50%;"></span>'+'<span class="pull-right">\
				<i class="icon-chevron-right"></i></span>').appendTo(row);
		});

		this.table.find("tr").click(function(event){
			$("#test_name_list .active").removeClass('active')
			$(this).addClass("active");
			me.render_test_details($(this)[0].innerText)
		})
	},
	render_test_details: function(test_name){
		var me = this;
		wn.call({
			method:"test.page.verification.verification.get_test_result",
			args:{"test_name":test_name},
			callback: function(r){
				me.render_resultset(r.message.test_details, r.message.test_name)
			}
		})
	},
	render_resultset:function(test_details, test_name){
		this.test_results = $(this.wrapper).find('#test_results');
		this.test_results.empty();
		var me = this;

		columns = [[wn._("Test Id"), 50], [wn._("Sample Number"), 50], 
			[wn._("Status"),50], [wn._("Dashboard"), 50]];

		this.table = $("<table class='table table-bordered'>\
			<thead><tr></tr></thead>\
			<tbody></tbody>\
		</table>").appendTo(this.test_results);

		$.each(columns, 
			function(i, col) {
			$("<th>").html(col[0]).css("width", col[1]+"px")
				.appendTo(me.table.find("thead tr"));
		});

		$.each(test_details, 
			function(i, test) {
			var row = $("<tr id="+i+">").appendTo(me.table.find("tbody"));
			$("<td>").html('<a href="#Form/'+test_name+'/'+test.name+'">'
				+test.name+'</a>').appendTo(row);
			$("<td>").html(test.sample_no).appendTo(row);
			$("<td>").html(test.workflow_state).appendTo(row);
			me.add_dashboard(row, test)
			
		});
	},
	add_dashboard:function(row, test){
		
		var me = this;
		$("<button class='btn btn-small btn-default'><i class='icon-dashboard'></i></button>")
			.appendTo($("<td>").appendTo(row))
			.attr("data-name", test.sample_no)
			.click(function() {
				me.open_dashboard($(this).attr("data-name"))
			});
	},
	open_dashboard:function(sample_no){
		var dashb = wn.model.make_new_doc_and_get_name('Test Case Dashboard');
		dashb = locals['Test Case Dashboard'][dashb];
		dashb.sample_no = sample_no
		loaddoc('Test Case Dashboard', dashb.name)
	}
})

var get_test_list = function(){
	
	return ['OST', 'OST R&DIFT','OST  PP  KV  Sediments',
		'Dissolve Gas','Furan Content','Aging Test',
		'P.C.B','inhibitor content','Metal In Oil']

	// return ['Physical Condition And Density', 'Density And Visual Examination',
	// 	'Resistivity and Dissipation', 'Dissolved Gas Analysis', 'Neutralization Value',
	// 	'Oxidation Inhibiters', 'Kinematic Viscosity', 'Corrossive Sulphur', 'Breakdown Voltage',
	// 	'Furan Content', 'Metal In Oil', 'Flash Point', 'Pour Point', 'Sediment', 'PCB']
}

wn.Notification = Class.extend({
	init:function(wrapper){
		this.wrapper = wrapper;
		this.body = $(this.wrapper).find(".user-settings");
		this.nottify_count_list = this.get_notification_count()
		this.set_span();
	},
	get_notification_count: function(){
		var me = this;
		wn.call({
			method:"test.page.verification.verification.get_notification_count",
			args:{"test_name_list":get_test_list()},
			callback: function(r){
				me.set_span(r.message.notification_count)
			}
		})
	},
	set_span:function(notification_count){
		//console.log(notification_count)
		for(key in notification_count){
			$("#"+key).text(notification_count[key])
		}
	}
})