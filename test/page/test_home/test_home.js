// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt"

wn.module_page["Test"] = [
	{
		title: wn._("Documents"),
		top: true,
		icon: "icon-copy",
		items: [
			{
				label: wn._("Breakdown Voltage"),
				description: wn._("Requests for items."),
				doctype:"Breakdown Voltage"
			},
			
			{
				label: wn._("Flash Point"),
				description: wn._("Requests for items."),
				doctype:"Flash Point"
			},
			// {
			// 	label: wn._("Interfacial Tension"),
			// 	description: wn._("Requests for items."),
			// 	doctype:"Interfacial Tension"
			// },
			{
				label: wn._("Neutralization Value"),
				description: wn._("Requests for items."),
				doctype:"Neutralization Value"
			},
			{
				label: wn._("Density And Visual Examination"),
				description: wn._("Requests for items."),
				doctype:"Density And Visual Examination"
			},
			{
				label: wn._("Dissolved Gas Analysis"),
				description: wn._("Requests for items."),
				doctype:"Dissolved Gas Analysis"
			},
			{
				label: wn._("Resistivity and Dissipation"),
				description: wn._("Requests for items."),
				doctype:"Resistivity and Dissipation"
			},
			{
				label: wn._("Physical Condition And Density "),
				description: wn._("Physical Condition,Density & Moisture calculation."),
				doctype:"Physical Condition And Density"
			},
			{
				label: wn._("Sediment "),
				description: wn._("Sediment & Precipitable Sludge."),
				doctype:"Sediment"
			}
		]
	},
	{
		title: wn._("Master"),
		icon: "icon-book",
		items:[
			{
				label: wn._("Tranformer"),
				description: wn._("Tranformer Details"),
				doctype:"Transformer"
			},
			{
				label: wn._("Sample Batch"),
				description: wn._("Batch Allocation For Group Of Samples"),
				doctype:"Sample Batch"
			},
			{
				label: wn._("Test Name"),
				description: wn._("Test Description"),
				doctype:"Test Name"
			},
			{
				label: wn._("Test Specification"),
				description: wn._("Predrfined Test Specification"),
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
				label: wn._("Normality "),
				description: wn._("Normality Of ALKOH For Neutralisation Value Calculation"),
				doctype:"Normality "
			}
		]
	},
	{
		title: wn._("Transaction"),
		icon: "icon-book",
		items: [
			// {
			// 	label: wn._("Outward Register"),
			// 	description: wn._("To track outword items"),
			// 	doctype:"Outward register"
			// },
			
			{
				label: wn._("Inward-Outward Entry"),
				description: wn._("To track Inword/Outward items"),
				doctype:"Stock Entry"
			},
			{
				label: wn._("Sample Entry"),
				description: wn._("To be filled while the sample is collected"),
				doctype:"Sample Entry"
			},
			{
				label: wn._("Test Allocation"),
				description: wn._("Sample registration including priority and test conduted on it"),
				doctype:"Test Allocation"
			},
			{
				label: wn._("Material Indent Form"),
				description: wn._("Requests for items."),
				doctype:"Material Indent Form"
			},
			{
				label: wn._("Sample Cretion"),
				description: wn._("Sample Creation/Sampling"),
				doctype:"Sample Creation"
			},
			{
				label: wn._("Sample Allocation"),
				description: wn._("Sample Allotment"),
				doctype: "Sample Allocation"
			},
			// {
			// 	label: wn._("Test Results"),
			// 	description: wn._("Test Results Record"),
			// 	doctype:"Test Results"
			// },
			{
				label: wn._("Request"),
				description: wn._("Request Details"),
				doctype:"Request"
			}
		]
	},
	{
		title: wn._("Other"),
		right: true,
		icon: "icon-bar-chart",
		items: [
			{
				label:wn._("Test Certificate"),
				doctype: "Test Certificate"
			},
			{
				label:wn._("Test Case Dashboard"),
				route:"Form/Test Case Dashboard"
			}
		]
	}
]

pscript['onload_test-home'] = function(wrapper) {
	wn.views.moduleview.make(wrapper, "Test");
}
