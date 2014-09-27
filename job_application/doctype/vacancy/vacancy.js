// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.apply_now = function(doc,cdt,cdn) {
	//console.log(doc.last_date_of_application);
	if(doc.post && doc.job_description && doc.last_date_of_application){
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var yyyy = today.getFullYear();
		if(dd<10) {
    		dd='0'+dd
		} 

		if(mm<10) {
   			mm='0'+mm
		} 
		today = yyyy+'-'+mm+'-'+dd;
		if(today<=doc.last_date_of_application){
			//console.log(today);
			//console.log(doc.last_date_of_application);
			var si = wn.model.make_new_doc_and_get_name('Job Application Form');
    		si = locals['Job Application Form'][si];
			loaddoc('Job Application Form', si.name);
		}
		else{
			msgprint("Sorry..!!!You can not apply for current job since last date of application was='"+doc.last_date_of_application+"' ")
		}
	}
	else{
		msgprint("Mandatory Fields should be filled before clicking on Apply Now button");
	}
	
}