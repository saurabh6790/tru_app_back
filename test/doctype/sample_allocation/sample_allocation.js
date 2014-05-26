
cur_frm.fields_dict.sample_allocation_detail.grid.get_field("tester").get_query = function(doc,cdt,cdn)
{	
  var d = locals[cdt][cdn];
  return {
		query: "test.doctype.sample_allocation.sample_allocation.get_employee",
		filters: {
			"level": 'Level 1',
			"test": d.test
		}
	}
}

cur_frm.fields_dict.sample_allocation_detail.grid.get_field("shift_incharge").get_query = function(doc,cdt,cdn)
{
  
  var d = locals[cdt][cdn];
  return {
		query: "test.doctype.sample_allocation.sample_allocation.get_employee",
		filters: {
			"level": 'Level 2',
			"test": d.test,
			"parent": d.tester
		}
	}
}

cur_frm.fields_dict.sample_allocation_detail.grid.get_field("lab_incharge").get_query = function(doc,cdt,cdn)
{	
  var d = locals[cdt][cdn];	
  return {
		query: "test.doctype.sample_allocation.sample_allocation.get_employee",
		filters: {
			"level": 'Level 3',
			"test": d.test,
			"parent": [d.tester, d.shift_incharge]
		}
	}
}

cur_frm.fields_dict.sample_id.get_query = function(doc, cdt, cdn) {
	return{
		query:"test.doctype.sample_allocation.sample_allocation.get_samples"
	}
}