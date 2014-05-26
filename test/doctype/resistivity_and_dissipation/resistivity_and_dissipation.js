cur_frm.cscript.sample_no=function(doc,cdt,cdn){
	get_server_fields('get_barcode',doc.sample_no,'',doc,cdt,cdn,1)
	refresh_field('bottle_no')
}

cur_frm.cscript.validate=function(doc,cdt,cdn){
	refresh_field('tan_value')
	refresh_field('sigma_value')
	refresh_field('resistivity_value')
}
