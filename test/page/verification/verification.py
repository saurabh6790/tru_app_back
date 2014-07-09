import webnotes
import re
mapper = {'OST': '`tabPhysical Condition And Density`, `tabMoisture Content`, `tabBreakdown Voltage`, `tabNeutralization Value`'}


@webnotes.whitelist()
def get_test_result(test_name):
	state = get_state()
	conditions = get_conditions(test_name, state)
	webnotes.conn.sql("""select `tabPhysical Condition And Density`.sample_no 
		from %(tabs)s """%{'tabs':mapper[test_name]})

	# test_details = webnotes.conn.sql("""select name,sample_no, workflow_state from `tab%s` 
	# 			where workflow_state = '%s'"""%(test_name[:re.search("\d",test_name).start()],state),as_dict=1)
	
	# return {
	# 	'test_details': test_details,
	# 	'test_name': test_name[:re.search("\d",test_name).start()]
	# }

def get_conditions(test_name, state):
	tablist = mapper[test_name].split(',')
	condition, sample_list = [], []

	for table in tablist:
		condition.append("%s.workflow_state = '%s'"%(table, state))

	return ' and '.join(condition)

@webnotes.whitelist()
def get_notification_count(test_name_list):
	state = get_state()

	test_name_list = eval(test_name_list)
	notification_count = {}

	for test in test_name_list:
		count = webnotes.conn.sql("""select count(*) from `tab%s` 
					where workflow_state = '%s'"""%(test,state),as_list=1)
		make_count_dir(count, notification_count, test)

	return{
		"notification_count":notification_count
	}

def get_state():
	roles = get_roles()

	state = ''
	if ['Shift Incharge'] in roles:
		state='Waiting For Approval'

	elif ['Lab Incharge'] in roles or ['Administrator'] in roles:
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