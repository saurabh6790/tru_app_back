// wn.pages['inward-outward'].onload = function(wrapper) { 
// 	wn.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'None',
// 		single_column: true
// 	});					
// }

wn.module_page["Inward-Outward"] = [
	{
		top: true,
		title: wn._("Documents"),
		icon: "icon-copy",
		items: [
			{
				label: wn._("Stock Entry"),
				description: wn._("Stock Entry Database."),
				doctype:"Stock Entry"
			},
			
		]
	}
]
pscript['onload_inward-outward'] = function(wrapper) {
	wn.views.moduleview.make(wrapper, "Inward-Outward");
}