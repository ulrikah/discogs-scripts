'''
1. Hent alle links fra label 

2. Legg til i txt-fil

3. Display i HTML-fil

'''



import discogs_client
import requests
import re 	#regex
import json
from bs4 import BeautifulSoup
import time

d = discogs_client.Client('YoutubeURLFromLabel/0.1')

# pattern to recognize youtube URLs
def getReleaseIdsFromLabel(labelId):
	
	label = d.label(labelId)
	releases = []
	for rel in label.releases:
		#do something
		releases.append(rel.id)

	return releases


def getReleaseTitleFromLabel(labelId):
	
	label = d.label(labelId)
	releases = []
	for rel in label.releases:
		#do something
		releases.append(rel.title)

	return releases


# find all links in html
def getURLFromRelease(id):
	r = requests.get('https://www.discogs.com/release/' + str(id))
	html = r.text
	soup = BeautifulSoup(html, 'html.parser') 		# seems to take too much time?
	txt = soup.find(id="dsdata") # the script id which contains YT links
	txt = txt.string
	txt = txt.split('return')[1].split('\n')[0][:-1].strip() # brute force to format the text
	j = json.loads(txt)
	urls = []
	for video in j['videos/macro:playlist']:
		urls.append(video['file'])
	return urls

if __name__ == '__main__':
	releases = getReleaseIdsFromLabel(321228)
	print(releases)
	allUrls = []
	for release in releases:
		allUrls.append(getURLFromRelease(release))

	print(allUrls)

