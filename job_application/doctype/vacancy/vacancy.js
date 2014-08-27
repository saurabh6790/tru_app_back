// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.apply_now = function(doc,cdt,cdn) {
	var si = wn.model.make_new_doc_and_get_name('Job Application Form');
    si = locals['Job Application Form'][si];
	loaddoc('Job Application Form', si.name);
	
}