#split by locality- has to match - hash them
import json, csv
from six import string_types

RUNNING_ON_TEST_SET = True

foursquare_data = json.load(open('foursquare_train_hard.json'))
locu_data = json.load(open('locu_train_hard.json'))
matches_data = csv.DictReader(open('matches_train_hard.csv')) #locu id is 1, foursquare is 2

foursquare_test_data = json.load(open('foursquare_test_hard.json'))
locu_test_data = json.load(open('locu_test_hard.json'))

#data cleanup
def process_data(data_set):
	for entry in data_set:
		for attr_name in entry:
			if entry[attr_name] == "":
				entry[attr_name] = None
			elif isinstance(entry[attr_name], string_types):
				entry[attr_name] = entry[attr_name].lower()
				if attr_name == 'street_address':
					entry[attr_name] = entry[attr_name].replace('/' , '')
					entry[attr_name] = entry[attr_name].replace('.' , '')
					entry[attr_name] = entry[attr_name].replace(' st ' , 'street ')
					entry[attr_name] = entry[attr_name].replace(' ave ' , 'avenue ')
					entry[attr_name] = entry[attr_name].replace(' blvd ' , 'boulevard ')
					entry[attr_name] = entry[attr_name].replace(' pl ' , 'plaza ')
					entry[attr_name] = entry[attr_name].replace(' w ' , ' west ')
					entry[attr_name] = entry[attr_name].replace(' e ' , ' east ')
					entry[attr_name] = entry[attr_name].replace(' s ' , ' south ')
					entry[attr_name] = entry[attr_name].replace(' n ' , ' north ')
					entry[attr_name] = entry[attr_name].replace(' boulevard ' , ' ')
				elif attr_name == 'website':
					entry[attr_name] = entry[attr_name].replace('/' , '')
				elif attr_name == 'phone':
					entry[attr_name] = entry[attr_name].replace('(' , '')
					entry[attr_name] = entry[attr_name].replace(')' , '')
					entry[attr_name] = entry[attr_name].replace(' ' , '')
					entry[attr_name] = entry[attr_name].replace('-' , '')

process_data(foursquare_data)
process_data(locu_data)
process_data(foursquare_test_data)
process_data(locu_test_data)


id_dict = {}
for row in matches_data:
	id_dict[row['locu_id']] = row['foursquare_id']

def str_attribute_match(foursquare_entry, locu_entry, attribute):
	if locu_entry[attribute] != None and foursquare_entry[attribute] != None and foursquare_entry[attribute] == locu_entry[attribute]:
		return 1
	return 0

def str_attribute_jaccard(foursquare_entry, locu_entry, attribute):
	if foursquare_entry[attribute] == None or locu_entry[attribute] == None:
		return 0

	fsq_set = set()
	locu_set = set()

	for elem in foursquare_entry[attribute].split(' '):
		fsq_set.add(elem)

	for elem in locu_entry[attribute].split(' '):
		locu_set.add(elem)

	return len(fsq_set.intersection(locu_set)) / float(len(fsq_set.union(locu_set)))

def is_match(foursquare_entry, locu_entry):
	if locu_entry['id'] in id_dict:
		return id_dict[locu_entry['id']] == foursquare_entry['id']
	else:
		return False

def long_attribute_match(foursquare_entry, locu_entry, attribute, threshold):
	if locu_entry[attribute] != None and foursquare_entry !=None  and abs(foursquare_entry[attribute] - locu_entry[attribute]) <= threshold:
		return 1
	else:
		return 0


def calculate_score(foursquare_entry, locu_entry):
	lat_long_thresh = 0.000005
	address_thresh = 0.8
	name_thresh = 0.15
	lat_long = long_attribute_match(foursquare_entry, locu_entry, 'longitude', lat_long_thresh) and long_attribute_match(foursquare_entry, locu_entry, 'latitude', lat_long_thresh)
	name = str_attribute_match(foursquare_entry, locu_entry, 'name')
	name_jaccard = str_attribute_jaccard(foursquare_entry, locu_entry, 'name')

	address = str_attribute_match(foursquare_entry, locu_entry, 'street_address')
	address_jaccard = str_attribute_jaccard(foursquare_entry, locu_entry, 'street_address')
	if address_jaccard >= address_thresh:
		address = 1
	phone = str_attribute_match(foursquare_entry, locu_entry, 'phone')
	zipcode = str_attribute_match(foursquare_entry, locu_entry, 'postal_code')
	website = str_attribute_match(foursquare_entry, locu_entry, 'website')

	if lat_long:
		return 1
	elif address and zipcode and name_jaccard >= name_thresh:
		return 1
	elif phone and name_jaccard >= name_thresh:
		return 1
	else:
		return (name * .5 + phone * .5 + address * .5 + website * .2 + zipcode * .4) / 1.4
	return 0

thresh = .9
total_matches = len(id_dict)
estimated_matches = 0

if RUNNING_ON_TEST_SET:
	matches_csv = open('matches_test.csv', 'wb')
	matches_csv.write('locu_id,foursquare_id\n')
	letter_dict = {}
	# Add all locu entries to dict, organized by first letter
	for locu_entry in locu_test_data:
		name = locu_entry['name']
		first_letter = name[0].lower()
		if first_letter not in letter_dict:
			letter_dict[first_letter] = list()
		letter_dict[first_letter].append(locu_entry)

	for foursquare_entry in foursquare_test_data:
		name = foursquare_entry['name'].lower()
		name_array = name.split(" ")
		first_letters = {}
		for elem in name_array:
			if elem[0] not in first_letters:
				first_letters[elem[0]] = elem[0]
		
	    # Now compare foursquare entry to locu entries in letter_dict
		for letter in first_letters:
			if letter in letter_dict:
				for locu_entry in letter_dict[letter]:
					score = calculate_score(foursquare_entry, locu_entry)			
					if score >= thresh:
						estimated_matches += 1
						matches_csv.write(locu_entry['id'] + "," + foursquare_entry['id'] + "\n")

	matches_csv.close()
else:
	true_pos = 0
	false_pos = 0
	estimated_matches = 0
	letter_dict = {}
	# Add all locu entries to dict, organized by first letter
	for locu_entry in locu_data:
		name = locu_entry['name'].lower()
		first_letter = name[0]
		if first_letter not in letter_dict:
			letter_dict[first_letter] = list()
		letter_dict[first_letter].append(locu_entry)

	for foursquare_entry in foursquare_data:
		name = foursquare_entry['name'].lower()
		name_array = name.split(" ")
		first_letters = {}
		for elem in name_array:
			if len(elem) > 0:
				if elem[0] not in first_letters:
					first_letters[elem[0]] = elem[0]
		
	    # Now compare foursquare entry to locu entries in letter_dict
		for letter in first_letters:
			if letter in letter_dict:
				for locu_entry in letter_dict[letter]:
					score = calculate_score(foursquare_entry, locu_entry)
					if score >= thresh:
						estimated_matches+= 1
						if is_match(foursquare_entry, locu_entry):
							true_pos+=1
						else:
							false_pos+=1
							# print(foursquare_entry)
							# print(locu_entry)

	if estimated_matches != 0:
		precision = float(true_pos) / estimated_matches
	else:
		precision = 0
	recall = float(estimated_matches) / total_matches

	print "Ground Truth Matches: " + str(total_matches)
	print "Estimated Matches: " + str(estimated_matches)
	print "True Positives: " + str(true_pos)
	print "False Positives: " + str(false_pos)
	print "Precision: " + str(precision)
	print "Recall: " + str(recall)
	print "F-Measure: " + str((2 * precision * recall) / (precision + recall))

