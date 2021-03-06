import urllib2
import json
import sys
import re
from url import submit_url

def start():
	if len(sys.argv) != 2:
		print "Please provide an ID"
		sys.exit()

	id = verify_id(sys.argv[1])
	if id == 0:
		print "Invalid ID"
		sys.exit()

	data = get_data(id)

	print data
	#submit(data)


def verify_id(id):
	regex = re.compile("^[A-D0-9][0-9]{3}$")
	if not regex.match(id):
		return 0

	data = json.load(urllib2.urlopen("https://s3-us-west-2.amazonaws.com/scee-interview-test/public/listing.json"))

	exists = False
	for game in data['catalog']:
		if (game['id'] == id):
			exists = True
			break

	if exists == True:
		return id
	else:
		return 0

def get_data(id):
	friends = [""]*4
	friends[0] = json.load(urllib2.urlopen("https://s3-us-west-2.amazonaws.com/scee-interview-test/public/ryu.json"))
	friends[1] = json.load(urllib2.urlopen("https://s3-us-west-2.amazonaws.com/scee-interview-test/public/ken.json"))
	friends[2] = json.load(urllib2.urlopen("https://s3-us-west-2.amazonaws.com/scee-interview-test/public/juri.json"))
	friends[3] = json.load(urllib2.urlopen("https://s3-us-west-2.amazonaws.com/scee-interview-test/public/akuma.json"))

	activity = []

	for i in range(len(friends)):
		for j in range(len(friends[i]['activity'])):
			if friends[i]['activity'][j]['game'] == id:
				friends[i]['activity'][j] = {
					"display_text": friends[i]['activity'][j]['display_text'],
					"timestamp": friends[i]['activity'][j]['timestamp'],
					"id": friends[i]['id']
				} # Reconstructs the activity entry to remove game ID and insert user ID
				activity.append(friends[i]['activity'][j])
	
	data = {
		"id": id,
		"activity": activity
	}
	return json.dumps(data)

def submit(data):
	header = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
	}
	req = urllib2.Request(submit_url, data, header)
	res = urllib2.urlopen(req)

	print res.read()

start()