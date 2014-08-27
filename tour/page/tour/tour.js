// wn.pages['tour'].onload = function(wrapper) { 
// 	wn.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'tour home',
// 		single_column: true
// 	});					
// }

wn.module_page["Tour"] = [
	{
		title: wn._("Tour Details Book"),
		top: true,
		icon: "icon-copy",
		items: [
			{
				label: wn._("Tour Details"),
				description : wn._("Tour in Sales."),
				doctype:"Tour Details"
			},
			{
				label: wn._("Tour Report"),
				description : wn._("Tour Report in Sales."),
				doctype:"Tour Report"
			},
		
		]
	},
]

pscript['onload_tour'] = function(wrapper) {
	wn.views.moduleview.make(wrapper, "Tour");
}

