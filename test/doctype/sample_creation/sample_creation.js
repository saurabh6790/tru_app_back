// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.s_entry = function(doc,cdt,cdn){
	if(doc.s_entry){
		get_server_fields('get_sample_entry_details',doc.s_entry,'',doc,cdt,cdn,1)
		refresh_field('bottle_no');
		refresh_field('bottles_barcodes');
	}

}