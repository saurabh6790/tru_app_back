import webnotes

sorting_dict = {}
sort_mapper = {'Ascending':'asc', 'Descending': 'desc'}

@webnotes.whitelist()
def get_tasnformer():
	return {
	'transfromer_id' : [d[0] for d in webnotes.conn.sql("""select name from tabTransformer""")]
	}

@webnotes.whitelist()
def save_sorting_order(parent=None, parent1=None, parent2=None, parent3=None):
	global sorting_dict 
	if parent:
		sorting_dict[parent] = parent1
	if parent2:
		sorting_dict[parent2] = parent3
	webnotes.errprint(sorting_dict)

@webnotes.whitelist()
def get_sample_entries(date, transfromer):
	conditions = get_conditions(date, transfromer)
	sort_order = get_sorting_order()

	return {
		'sample_entry' : get_sample_entries_data(conditions, sort_order)
	}

def get_conditions(date, transfromer):
	condition = ''
	conditions = []

	if date:
		conditions.append("date = '%s'"%(dormat_date(date)))

	if transfromer and transfromer!= 'Select Transformer...':
		conditions.append("functional_location= '%s'"%(transfromer))

	if conditions:
		condition = 'and '.join(conditions)

	if condition:
		return 'and '+condition

def dormat_date(date):
	import datetime
	try:
		return datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
	except e:
		webnotes.msgprint(e,raise_exception=1)

def get_sorting_order():
	sort_list = []
	if sorting_dict:
		for key in sorting_dict:
			sort_string = ''
			sort_string += '%s %s '%(key.lower().replace(' ', '_'), sort_mapper[sorting_dict[key]])
			sort_list.append(sort_string)

	if sort_list:
		return ' order by ' + ', '.join(sort_list)

def get_sample_entries_data(conditions, sort_order):
	if not conditions:
		conditions = ''

	if not sort_order:
		sort_order = ''

	return webnotes.conn.sql("""select name, ifnull(plant,'---') as plant, 
				ifnull(functional_location,'----') as functional_location, ifnull(sub_station,'---') as sub_station, ifnull(rating, '---') as rating from `tabSample Entry` 
				where ifnull(docstatus,'') != 2 and ifnull(is_sample_generated,'No') != 'Yes'
				%(conditions)s %(sort_order)s """%{"conditions": conditions, 'sort_order': sort_order}, as_dict=1, debug=1)

@webnotes.whitelist()
def sample_generation(sample_entries):
	sample_entries = eval(sample_entries)	
	for sample in sample_entries:
		generate_sample(sample)
	return{
		'sample_entries':sample_entries
	}

def generate_sample(sample):
	from webnotes.model.doc import Document
	d = Document('Sample')
	d.sample_entry = sample['name']
	d.barcode = webnotes.conn.get_value("Sample Entry", sample['name'], 'bottle_list')
	d.client_name = webnotes.conn.get_value('Sample Entry', sample['name'], 'client_name')
	d.temperature = webnotes.conn.get_value('Sample Entry', sample['name'], 'testing_temperature')
	d.save()
	update_sample_entry(sample['name'])
	update_sample(sample, d.name)

def update_sample_entry(sample_entry_name):
	webnotes.conn.sql("""update `tabSample Entry` 
							set is_sample_generated = 'Yes' 
						where name = '%s'"""%(sample_entry_name),debug=1)
	webnotes.conn.sql("commit")

def update_sample(sample, sample_id):
	sample['sample_id'] = sample_id