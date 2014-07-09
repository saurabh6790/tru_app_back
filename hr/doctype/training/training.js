// For getting user_id from employee table on the trigger of employee id
cur_frm.add_fetch('trainners', 'user_id', 'user_id');

cur_frm.add_fetch('employee', 'employment_type', 'e_type');

cur_frm.add_fetch('employee', 'employee_name', 'employee_name');

//For getting all the test name from on the trigger of employee
cur_frm.cscript.employee = function(doc,cdt,cdn){
	if(doc.training_level && doc.employee){
    //console.log("in employee trigger")
	 	get_server_fields('get_training_details','','',doc,cdt,cdn,1,function(r,rt){refresh_field('training')});
 	}
 	// else
 		// msgprint("Traning Level and Type of Employee Cannot Be Blank")
}


// cur_frm.get_field("employee").get_query=function(doc,cdt,cdn)
// {
//    return "select employee from `tabEmployee` where designation='Test Engineer' "

// }


//For avoiding the same name in main form and in trainners child table in Traning DocType-return query on child table
cur_frm.fields_dict.trainner.grid.get_field("trainners").get_query = function(doc,cdt,cdn)
{
	return "select employee from `tabEmployee` where employee!='"+doc.employee+"'"	
}

cur_frm.fields_dict.trainner.grid.get_field("trainners").get_query = function(doc,cdt,cdn)
{
  return "select employee from `tabEmployee` where employee!='"+doc.employee+"'"  
}


cur_frm.cscript.send_notification = function(doc, dt, dn) {
  if (doc.employee && doc.name && doc.training_date)
  {
     	return wn.call({
               	method: "hr.doctype.training.training.send_notification",
              	 args: {
                       	employee: doc.employee,
                        docname: doc.name,
                        date:doc.training_date
               	}
      	 });
  }
  else
    msgprint("Employee Name,Training Date are mandatory")
}



cur_frm.cscript.refresh = function(doc,cdt,cdn){
  if(doc.__islocal){
    hide_field('send_notification'); 
    
  }
  else{
    unhide_field('send_notification');
  }
}