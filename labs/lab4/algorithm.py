#split by locality- has to match - hash them
import json


foursquare_file = open('foursquare_train_hard.json')
foursquare_data = json.load(foursquare_file)
foursquare_file.close()

locu_file = open('locu_train_hard.json')
locu_data = json.load(locu_file)
locu_file.close()


print len(foursquare_data)
print len(locu_data)

count = 0
for locu_entry in locu_data:
	for foursquare_entry in foursquare_data:
		if locu_entry['name'] == foursquare_entry['name']:
			count+=1

print count
