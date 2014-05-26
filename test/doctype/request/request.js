cur_frm.cscript.onload = function(doc,dt,dn){
	//if(doc.request_from =='Self'){

		//console.log(user)
		doc.requestor=user;
		doc.executor=user;
		refresh_field('requestor');
		refresh_field('executor');
	//}
}