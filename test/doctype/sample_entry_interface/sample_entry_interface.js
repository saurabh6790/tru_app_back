// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


//to fetch all the details against the functional location from the transformer master
cur_frm.add_fetch('functional_location', 'client_name','client_name');

cur_frm.add_fetch('functional_location', 'plant','plant');

cur_frm.add_fetch('functional_location', 'sub_station','sub_station');

cur_frm.add_fetch('functional_location', 'serial_no','serial_no');

cur_frm.add_fetch('functional_location', 'make','make');

cur_frm.add_fetch('functional_location', 'phase','phase');

cur_frm.add_fetch('functional_location', 'rating','rating');



cur_frm.cscript.refresh = function(doc) {
	cur_frm.disable_save();
}

cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_bottle_no',doc.bottle,'',doc,cdt,cdn,1);
  refresh_field('bottle_list');
}

cur_frm.cscript.clear = function(doc){
	return wn.ui.toolbar.clear_cache();
}

// for getting functional location against the customer involved in the inward stock entry
cur_frm.fields_dict['functional_location'].get_query=function(doc,cdt,cdn)
{
	return{
		query:"test.doctype.sample_entry_interface.sample_entry_interface.get_functional_location",
		filters:{
			"inward_stock_entry":doc.inward_stock_entry
		}
	}
}


// for getting bootle no. i-e barcode involved in the inward stock entry
cur_frm.fields_dict['bottle'].get_query=function(doc,cdt,cdn)
{
	return{
		query:"test.doctype.sample_entry_interface.sample_entry_interface.get_bottle_no",
		filters:{
			"inward_stock_entry":doc.inward_stock_entry
		}
	}
}