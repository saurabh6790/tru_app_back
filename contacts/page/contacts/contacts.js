// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt"

wn.module_page["Contacts"] = [
	{
		top: true,
		title: wn._("Documents"),
		icon: "icon-copy",
		items: [
			{
				label: wn._("Customer"),
				description: wn._("Customer database."),
				doctype:"Customer"
			},
			{
				label: wn._("Supplier"),
				description: wn._("Database of potential customers."),
				doctype:"Supplier"
			},
			{
				label: wn._("Contacts"),
				description: wn._("Potential opportunities for selling."),
				doctype:"Contact"
			},
		]
	}
]

pscript['onload_contacts'] = function(wrapper) {
	wn.views.moduleview.make(wrapper, "Contacts");
}