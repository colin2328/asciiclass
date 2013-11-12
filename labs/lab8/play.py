import csv

def add_to_dict(address, diction):
	if diction.has_key(address):
		diction[address] += 1
	else:
		diction[address] = 1

in_csv = open('pickups_train.csv')
csv_reader = csv.DictReader(in_csv)
fields = csv_reader.fieldnames

interest_reader = csv.DictReader(open('interestpoints.csv'))
fields2 = interest_reader.fieldnames
print fields2

print round(10.55551657498455, 5)

print fields
addresses = {}
x = 0
interest_lat_longs = {}
for row in interest_reader:
	lat = round(float(row['LAT']), 5)
	longitude = round(float(row['LONG']), 5)
	lat_long = str(lat) + '_' + str(longitude)

	add_to_dict( lat_long, interest_lat_longs)


for row in csv_reader:
	if x > 1000:
		break
	lat = round(float(row['latitude']), 5)
	lat = round(float(row['longitude']), 5)
	lat_long = str(lat) + '_' + str(longitude)

	add_to_dict(lat_long, addresses)
	x +=1


print len(addresses)
print (addresses)
print len(interest_lat_longs)
print (interest_lat_longs)


