cur_frm.cscript.normality=function(doc, cdt, cdn){
	get_server_fields('retrieve_normality_values','','',doc,cdt,cdn,1,function(){
		refresh_field(['normality_of_hcl','volume','koh_volume','normality_of_koh','method'])
	})
}



cur_frm.cscript.sample_no=function(doc,cdt,cdn){
  var d = locals[cdt][cdn];
  return get_server_fields('get_barcode', d.sample_no, 'neutralisation_test_details', doc, cdt, cdn, 1);
  refresh_field('bottle_no')
}

cur_frm.cscript.calculate_reported_value=function(doc,cdt,cdn){
	var d = locals[cdt][cdn]
	if (d.ml_consumes_of_alkoh && doc.normality_of_koh && d.density_of_oil && d.volume_of_oil){
		d.reported_value=calculate_reported_value(d.ml_consumes_of_alkoh,doc.normality_of_koh,d.density_of_oil,d.volume_of_oil)
}
	refresh_field('neutralisation_test_details')
}

cur_frm.cscript.density_of_oil=function(doc, cdt, cdn){
	cur_frm.cscript.calculate_reported_value(doc, cdt, cdn)
}
cur_frm.cscript.ml_consumes_of_alkoh=function(doc, cdt, cdn) {
	cur_frm.cscript.calculate_reported_value(doc, cdt, cdn)
}
cur_frm.cscript.volume_of_oil=function(doc, cdt, cdn){
	cur_frm.cscript.calculate_reported_value(doc, cdt, cdn)
}

function calculate_reported_value(ml_consumes_of_alkoh, normality_of_koh, density_of_oil, volume_of_oil){
	return (56.1*parseFloat(ml_consumes_of_alkoh)*parseFloat(normality_of_koh)/parseFloat(density_of_oil)*parseFloat(volume_of_oil)).toFixed(2);
}