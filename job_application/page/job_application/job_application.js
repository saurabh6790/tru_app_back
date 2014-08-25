// wn.pages['job-application'].onload = function(wrapper) { 
// 	wn.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'None',
// 		single_column: true
// 	});					
// }



// wn.pages['inward-outward'].onload = function(wrapper) { 
// 	wn.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'None',
// 		single_column: true
// 	});					
// }

wn.module_page["Job Application"] = [
	{
		top: true,
		title: wn._("Job Vacancy"),
		icon: "icon-copy",
		items: [
			{
				label: wn._("Vacancy"),
				description: wn._("Vacancy Database."),
				doctype:"Vacancy"
			},
			
		]
	}
]
pscript['onload_job-application'] = function(wrapper) {
	wn.views.moduleview.make(wrapper, "Job Application");
}