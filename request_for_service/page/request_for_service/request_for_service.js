// wn.pages['request-for-service'].onload = function(wrapper) { 
// 	wn.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'None',
// 		single_column: true
// 	});					
// }


wn.module_page["Request For Service"] = [
	{
		top: true,
		title: wn._("Documents"),
		icon: "icon-copy",
		items: [
			{
				label: wn._("Request"),
				description: wn._("Request Details."),
				doctype:"Request"
			},
			
		]
	}
]
pscript['onload_request-for-service'] = function(wrapper) {
	wn.views.moduleview.make(wrapper, "Request For Service");
}