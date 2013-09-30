#split by locality- has to match - hash them
import json, csv

RUNNING_ON_TEST_SET = True

foursquare_data = json.load(open('foursquare_train_hard.json'))
locu_data = json.load(open('locu_train_hard.json'))
matches_data = csv.DictReader(open('matches_train_hard.csv')) #locu id is 1, foursuare is 2

foursquare_test_data = json.load(open('foursquare_test_hard.json'))
locu_test_data = json.load(open('locu_test_hard.json'))

id_dict = {}
for row in matches_data:
	id_dict[row['locu_id']] = row['foursquare_id']

def str_attribute_match(foursquare_entry, locu_entry, attribute):
	if foursquare_entry[attribute] == "":
		foursquare_entry[attribute] = None
	if locu_entry[attribute] == "":
		locu_entry[attribute] = None
	if locu_entry[attribute] != None and foursquare_entry[attribute] != None:
#		foursquare_entry[attribute].lower()
#		foursquare_entry[attribute].replace('/' , '')
#		foursquare_entry[attribute].replace(' st. ' , ' ')
#		foursquare_entry[attribute].replace(' street ' , ' ')
#		foursquare_entry[attribute].replace(' ave ' , ' ')
#		foursquare_entry[attribute].replace(' blvd. ' , ' ')
#		foursquare_entry[attribute].replace(' avenue ' , ' ')
#		foursquare_entry[attribute].replace(' w. ' , ' ')
#		foursquare_entry[attribute].replace(' e. ' , ' ')
#		foursquare_entry[attribute].replace(' s. ' , ' ')
#		foursquare_entry[attribute].replace(' n. ' , ' ')
#		foursquare_entry[attribute].replace(' boulevard ' , ' ')
#
#		locu_entry[attribute].lower()
#		locu_entry[attribute].replace('/' , '')
#		locu_entry[attribute].replace(' st. ' , ' ')
#		locu_entry[attribute].replace(' street ' , ' ')
#		locu_entry[attribute].replace(' ave ' , ' ')
#		locu_entry[attribute].replace(' blvd. ' , ' ')
#		locu_entry[attribute].replace(' avenue ' , ' ')
#		locu_entry[attribute].replace(' w. ' , ' ')
#		locu_entry[attribute].replace(' e. ' , ' ')
#		locu_entry[attribute].replace(' s. ' , ' ')
#		locu_entry[attribute].replace(' n. ' , ' ')
#		locu_entry[attribute].replace(' boulevard ' , ' ')

		if foursquare_entry[attribute] == locu_entry[attribute]:
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
	if foursquare_entry[attribute] == "":
		foursquare_entry[attribute] = None
	if locu_entry[attribute] == "":
		locu_entry[attribute] = None
	if locu_entry[attribute] != None and foursquare_entry !=None  and abs(foursquare_entry[attribute] - locu_entry[attribute]) <= threshold:
		return 1
	else:
		return 0


def calculate_score(foursquare_entry, locu_entry):
	lat_long_thresh = 0.000005
	lat_long = long_attribute_match(foursquare_entry, locu_entry, 'longitude', lat_long_thresh) and long_attribute_match(foursquare_entry, locu_entry, 'latitude', lat_long_thresh)
	name = str_attribute_match(foursquare_entry, locu_entry, 'name')
	address = str_attribute_match(foursquare_entry, locu_entry, 'street_address')
	address_jaccard = str_attribute_jaccard(foursquare_entry, locu_entry, 'street_address')
	if address_jaccard > 0.7:
		address = 1
	phone = str_attribute_match(foursquare_entry, locu_entry, 'phone')
	zipcode = str_attribute_match(foursquare_entry, locu_entry, 'postal_code')
	website = str_attribute_match(foursquare_entry, locu_entry, 'website')

	if lat_long:
		return 1
	elif address and zipcode and name:
		return 1
	else:
		return name * .5 + phone * .2 + address * .5 + website * .2 + zipcode * .4

thresh = .7
total_matches = len(id_dict)
estimated_matches = 0

if RUNNING_ON_TEST_SET:
	matches_csv = open('matches_test.csv', 'wb')
	matches_csv.write('locu_id,foursquare_id\n')
	for locu_entry in locu_test_data:
		for foursquare_entry in foursquare_test_data:
			score = calculate_score(foursquare_entry, locu_entry)
			if score >= thresh:
				estimated_matches += 1
				matches_csv.write(locu_entry['id'] + "," + foursquare_entry['id'] + "\n")

	matches_csv.close()
else:
	true_pos = 0
	false_pos = 0
	for locu_entry in locu_data:
		for foursquare_entry in foursquare_data:
			score = calculate_score(foursquare_entry, locu_entry)
			if score >= thresh:
				estimated_matches+= 1
				if is_match(foursquare_entry, locu_entry):
					true_pos+=1
				else:
					false_pos+=1
					# print(foursquare_entry)

	if estimated_matches != 0:
		precision = float(true_pos) / estimated_matches
	else:
		precision = 0
	recall = float(estimated_matches) / total_matches

	print "Estimated Matches: " + str(estimated_matches)
	print "True Positives: " + str(true_pos)
	print "False Positives: " + str(false_pos)
	print "Precision: " + str(precision)
	print "Recall: " + str(recall)
	print "F-Measure: " + str((2 * precision * recall) / (precision + recall))
