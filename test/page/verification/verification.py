import webnotes
import re
from webnotes.model.code import get_obj

mapper = {'OST': ['`tabPhysical Condition And Density`', '`tabMoisture Content`', '`tabBreakdown Voltage`', 
						'`tabNeutralization Value`'],
		'OST R&D IFT':['`tabPhysical Condition And Density`', '`tabResistivity and Dissipation`', 
						'`tabInterfacial Tension`', '`tabNeutralization Value`'],
		'OST PP KV Sediments' : ['`tabPhysical Condition And Density`','`tabFlash Point`','`tabPour Point`',
						'`tabKinematic Viscosity`','`tabTest Of Extract`'],
		'Dissolve Gas':['`tabPhysical Condition And Density`','`tabFlash Point`','`tabDissolved Gas Analysis`'],
		'Furan Content':['`tabPhysical Condition And Density`','`tabDissolved Gas Analysis`','`tabFuran Content`'],
		'Aging Test' :['`tabPhysical Condition And Density`','`tabCorrossive Sulphur`']
		}

child_mapper = {'`tabNeutralization Value`': ['`tabNeutralization Test Details`']}
# or ['Administrator'] in roles
@webnotes.whitelist()
def get_test_result(test_name):
	webnotes.errprint([test_name])
	if re.search("\d",test_name):
		test_name = test_name[:re.search("\d",test_name).start()]

	state = get_state()
	conditions, chld_tab = get_conditions(mapper[test_name], state)

	test_details = webnotes.conn.sql("""select distinct %(tab)s.sample_no,%(tab)s.workflow_state 
		from %(tabs)s %(chld_tab)s where %(cond)s"""%{'tabs':' ,'.join(mapper[test_name]), 
		'cond':conditions, 'tab': mapper[test_name][0], 'chld_tab': chld_tab}, as_dict=1,debug=1)

	return {
		'test_details': test_details
		# 'test_name': test_name[:re.search("\d",test_name).start()]
	}

def get_conditions(test_name, state):
	condition, sample_cond, chld_tab = [], [], []
	length = len(test_name)
	for index in range(0, length):
		if index < length-1:
			if not check_for_escape_test(test_name, index, sample_cond, chld_tab):
				sample_cond.append('%s.sample_no = %s.sample_no'%(test_name[index], test_name[index+1]))
			
		if webnotes.session.user!='Administrator': 
			condition.append("%s.workflow_state = '%s'"%(test_name[index], state))
	condition.extend(sample_cond)
	return ' and '.join(condition), ', ' + ','.join(chld_tab)

def check_for_escape_test(test_name, index, sample_cond, chld_tab):
	webnotes.errprint([test_name[index], test_name[index+1]])
	if test_name[index] in child_mapper: 
		replace_test(test_name, index, sample_cond, chld_tab)
		index = index + 1
		return True

	if test_name[index+1] in child_mapper:
		replace_test(test_name, index+1, sample_cond, chld_tab)
		index = index + 1
		return True

	return False

def replace_test(test_name, index, sample_cond, chld_tab):
	replaced_test = test_name[index]
	child_test = child_mapper[test_name[index]][0]
	chld_tab.append(child_mapper[test_name[index]][0])
	sample_cond.append('%s.sample_no = %s.sample_no'%(test_name[index-1], child_mapper[test_name[index]][0]))
	sample_cond.append('%s.parent = %s.name'%(child_test, replaced_test))

	webnotes.errprint(['%s.parent = %s.name'%(child_test, replaced_test)])
	

@webnotes.whitelist()
def get_notification_count(test_name_list):
	notification_count = {}
	state = get_state()
	for test_name in mapper:
		conditions = get_conditions(mapper[test_name], state)
		# webnotes.errprint(test_name)
		count =  webnotes.conn.sql("""select count(distinct %(tab)s.sample_no )
						from %(tabs)s where %(cond)s"""%{'tabs':' ,'.join(mapper[test_name]), 
						'cond':conditions, 'tab': mapper[test_name][0]}, as_list=1,debug=1)

		make_count_dir(count, notification_count, test_name)

	return{
		"notification_count":notification_count
	}

def get_state():
	roles = get_roles()

	state = ''
	if ['Shift Incharge'] in roles:
		state='Waiting For Approval Of Shift Incharge'

	elif ['Lab Incharge'] in roles :
		state='Waiting For Approval Of  Lab Incharge'

	return state

@webnotes.whitelist()
def roles():
	return {
		'roles': get_roles()
	}

def get_roles():
	if webnotes.session.user == 'Administrator':
		return [['Administrator']]

	else:
		return webnotes.conn.sql("""Select r.role from `tabProfile` p, `tabUserRole` r 
			where p.name='%s' and r.parent=p.name """%(webnotes.session.user),as_list=1)

def make_count_dir(count, notification_count, test):
	if count:
		if count[0][0] != 0:
			notification_count[test.replace(' ','_')] = count[0][0]

@webnotes.whitelist()
def get_tasnformer(test_names):
	samples = get_samples(test_names)
	transfromer_id = get_tasnformers(samples)

	return {
		'transfromer_id':[d[0] for d in transfromer_id]
	}

def get_samples(test_names):
	samples = []
	test_names = eval(test_names)
	for test in test_names:
		sample = webnotes.conn.sql(""" select sample_no from `tab%s` 
			where workflow_state = '%s' and sample_no is not null 
			and length(trim(sample_no)) != 0"""%(test, get_state()), as_list=1)
		[samples.extend(el) for el in sample]

	return samples

def get_tasnformers(samples):
	return webnotes.conn.sql("""select functional_location from `tabSample Entry` 
		where name in ( select sample_entry from tabSample 
			where name in ('%s'))"""%(','.join(samples)),as_list=1)

@webnotes.whitelist()
def get_certi(transfromer):
	return 	{
		'certi' : webnotes.conn.sql("select name from `tabTest Certificate` where sr_no = '%s'"%(transfromer), as_list=1)
	}

@webnotes.whitelist()
def get_test_details(sample_no):
	test = get_obj('Test Case Dashboard', 'Test Case Dashboard').get_sample_wise_test(sample_no)
	result = get_obj('Test Case Dashboard', 'Test Case Dashboard').get_test_wise_results(test, sample_no)
	return {
		"result": result
	}

@webnotes.whitelist()
def update_doc(dt, dn):
	role = get_roles()

	if ['Shift Incharge'] in role:
		webnotes.conn.sql("""update `tab%s` 
				set workflow_state = 'Waiting For Approval Of  Lab Incharge' 
				where name = '%S'"""%(dt, dn))
		webnotes.conn.commit()

	elif ['Administrator'] in role:
		get_obj(dt,dn).on_submit()