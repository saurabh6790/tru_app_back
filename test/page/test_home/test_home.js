// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt"

wn.module_page["Test"] = [
	{
		title: wn._("Test Result Book"),
		icon: "icon-book",
		items: [
			{
				label: wn._("Breakdown Voltage"),
				description: wn._("Requests for items."),
				root:('/app.html#Form/Page/test-result-book'),
				doctype:"Breakdown Voltage"
			},
			
			{
				label: wn._("Flash Point"),
				description: wn._("Requests for items."),
				root:('/app.html#Form/Page/test-result-book'),
				doctype:"Flash Point"
			},
			
			{
				label: wn._("Neutralization Value"),
				description: wn._("Requests for items."),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Neutralization Value"
			},
			{
				label: wn._("Moisture Content"),
				description: wn._("Moisture Content Test Details."),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Moisture Content"
			},
			{
				label: wn._("Interfacial Tension"),
				description: wn._("Interfacial Tension Test Details."),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Interfacial Tension"
			},
			{
				label: wn._("Dissolved Gas Analysis"),
				description: wn._("Requests for items."),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Dissolved Gas Analysis"
			},
			{
				label: wn._("Resistivity and Dissipation"),
				description: wn._("Requests for items."),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Resistivity and Dissipation"
			},
			{
				label: wn._("Physical Condition And Density "),
				description: wn._("Physical Condition & Density calculation."),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Physical Condition And Density"
			},
			
			{
				label: wn._("Kinematic Viscosity"),
				description: wn._("Kinematic Viscosity Details."),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Kinematic Viscosity"
			},
			{
				label: wn._("Pour Point"),
				description: wn._("Pour point Test Details"),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Pour Point"
			},
			{
				label: wn._("PCB"),
				description: wn._("PCB Test Details"),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"PCB"
			},
			
			{
				label: wn._("Oxidation Inhibiters"),
				description: wn._("Oxidation Inhibiters Test Details"),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Oxidation Inhibiters"
			},
			{
				label: wn._("Metal In Oil"),
				description: wn._("Metal In Oil Test Details"),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Metal In Oil"
			},
			{
				label: wn._("Test Of Extract"),
				description: wn._("Testing Of Extract Test Details."),
				root:('/app.html#Form/Page/test-result-book'),
				doctype:"Test Of Extract"
			},
			{
				label: wn._("Furan Content"),
				description: wn._(" Furan Conten Test Details."),
				root:('/app.html#Form/Page/test-result-book'),
				doctype:"Furan Content"
			},
			{
				label: wn._("Corrossive Sulphur"),
				description: wn._("Corrossive Sulphur Test Details"),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Corrossive Sulphur"
			},

			{
				label: wn._("Test Preparation"),
				description: wn._("First Step as Preparation of sample."),
				root:'/app.html#Form/Page/test-result-book',
				doctype:"Test Preparation"
			},
		 ]
	},
	{
		title: wn._("Master"),
		right: true,
		icon: "icon-book",
		items:[
			{
				label: wn._("Transformer"),
				description: wn._("Transformer Details"),
				doctype:"Transformer"
			},
			// {
			// 	label: wn._("Sample Batch"),
			// 	description: wn._("Batch Allocation For Group Of Samples"),
			// 	doctype:"Sample Batch"
			// },
			{
				label: wn._("Test Name"),
				description: wn._("Test Description"),
				doctype:"Test Name"
			},
			{
				label: wn._("Test Specification"),
				description: wn._("Predefined Test Specification"),
				doctype:"Test Specification"
			},
			{
				label: wn._("Test Group"),
				description: wn._("Group of tests"),
				doctype: "Test Group"
			},
			{
				label: wn._("GAS"),
				description: wn._("Gas Master for Dissolved Gas Analysis"),
				doctype: "Gas"
			},
			{
				label: wn._("Request Type"),
				description: wn._("Request Type Master"),
				doctype: "Request Type"
			},
			{
				label: wn._("Normality"),
				description: wn._("Normality For Neutralization Value."),
				doctype:"Normality"
			}
		]
	},
	{
		title: wn._("Transaction"),
		right: true,
		icon: "icon-book",
		items: [
			// {
			// 	label: wn._("Outward Register"),
			// 	description: wn._("To track outword items"),
			// 	doctype:"Outward register"
			// },
			
			// {
			// 	label: wn._("Inward/Outward Entry"),
			// 	description: wn._("To track Inword/Outward items"),
			// 	doctype:"Stock Entry"
			// },
			{
				label: wn._("Sample Entry"),
				description: wn._("To be filled while the sample is collected"),
				doctype:"Sample Entry"
			},
			// {
			// 	label: wn._("Test Allocation"),
			// 	description: wn._("Sample registration including priority & test conduted on it"),
			// 	doctype:"Test Allocation"
			// },
			{
				label: wn._("Material Indent Form"),
				description: wn._("Requests for items."),
				doctype:"Material Indent Form"
			},
			// {
			// 	label: wn._("Sample Cretion"),
			// 	description: wn._("Sample Creation/Sampling"),
			// 	doctype:"Sample Creation"
			// },
			{
				label: wn._("Sample Allocation"),
				description: wn._("Sample Allotment To Tester"),
				doctype: "Sample Allocation"
			},
			{
				label: wn._("Sample Allocation To Lab"),
				description: wn._("Sample Allocation To Lab Details"),
				doctype:"Sample Allocation To Lab"
			}
			// {
			// 	label: wn._("Request"),
			// 	description: wn._("Request Details"),
			// 	doctype:"Request"
			// }
		]
	},
	{
		title: wn._("Other"),
		right: true,
		icon: "icon-bar-chart",
		items: [
			
						{
				label:wn._("Sample Entry Interface"),
				route:"Form/Sample Entry Interface"
			},
			{
				label:wn._("Test Allocation Interface"),
				route:"Form/Test Allocation Interface"
			},
			// {
			// 	label:wn._("Test Case Dashboard"),
			// 	route:"Form/Test Case Dashboard"
			// },
			{
				label:wn._("Test Certificate"),
				doctype: "Test Certificate"
			}
		]
	}
]

pscript['onload_test-home'] = function(wrapper) {
	// wn.views.moduleview.popup(wrapper);
	wn.views.moduleview.make(wrapper, "Test");
	// dialog()
	// alert("Done")
}
function dialog(){
	console.log("test")
	var d = new wn.ui.Dialog({
		title:wn._('Get patient'),
		fields: [
			{fieldtype:'Data', fieldname:'patient_id', label:wn._('Patient Id'), reqd:true, 
				description: wn._("Enter Patient Global Id")+
				wn._("Enter Patient Global Id")},
			{fieldtype:'Button', fieldname:'fetch_patient', label:wn._('Fetch Patient') }
		]
	})
	var fd = d.fields_dict;
	$(fd.fetch_patient.input).click(function() {
			var btn = this;
			$(btn).set_working();
			var patient_id  = d.get_values();
			if(!patient_id) return;	
			return wn.call({
				args: patient_id,
				method:'clinical.doctype.patient_encounter_entry.patient_encounter_entry.get_patient',
				callback: function(r) {
					$(btn).done_working();
					d.hide();
				}
			});
		});

	d.show();
}