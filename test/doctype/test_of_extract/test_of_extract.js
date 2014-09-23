// Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


cur_frm.cscript.add = function(doc,cdt,cdn){

  get_server_fields('add_equipment',doc.equipment,'',doc,cdt,cdn,1);
  refresh_field('equipment_list')
}

cur_frm.fields_dict['sample_no'].get_query=function(doc,cdt,cdn)
{
	if(doc.test_preparation){
  		return{
    		query:"test.doctype.test_of_extract.test_of_extract.get_sample_no",
    		filters:{
				"test_preparation":doc.test_preparation
			}
    
  		}
	}
}

