cur_frm.cscript.sample_no=function(doc,cdt,cdn){

	get_server_fields('get_details','','',doc,cdt,cdn,1,function(r){refresh_field(['certificate_test_details','sr_no','make','rating','ratio'])})
}