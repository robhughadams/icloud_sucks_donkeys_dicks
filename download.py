import json, urllib

stream_id = 'ADG6XBubGx0KND'
base_url = 'https://p13-sharedstreams.icloud.com/' + stream_id + '/sharedstreams/'

url = base_url + 'webstream'
print 'downloading photo list from ' + url
post_data = '{"streamCtag":null}'
response = urllib.urlopen(url, post_data)
with open('photo_list.json', 'w') as f:
	f.write(response.read())

with open('photo_list.json') as f:
	data = json.load(f)

photos = data['photos']
guids = [item['photoGuid'] for item in photos]

chunk = 20
batches = zip(*[iter(guids)]*chunk)

for batch in batches:
	url = base_url + 'webasseturls'
	print 'downloading photo urls from ' + url
	post_data = '{"photoGuids":["' + '","'.join(batch) + '"]}'
	response = urllib.urlopen(url, post_data)

	data = json.load(response)
	locations = data['locations']
	items = data['items']
	for key, item in items.iteritems():
		location = item['url_location']
		host = locations[location]['hosts'][0]
		url = 'https://' + host + item['url_path']
		print 'downloading photo from ' + url
		urllib.urlretrieve(url, key + '.jpeg')

