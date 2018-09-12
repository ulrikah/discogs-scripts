'''
1. Hent alle links fra label 

2. Display i HTML-fil

'''

import sys
import discogs_client
import requests
import re 	#regex
import json
from bs4 import BeautifulSoup
import time

d = discogs_client.Client('YoutubeURLFromLabel/0.1')

def getReleaseIdsFromLabel(labelId):
	label = d.label(labelId)
	releases = []
	for rel in label.releases:
		releases.append(rel.id)
	return releases


def getReleaseTitleFromLabel(labelId):
	label = d.label(labelId)
	releases = []
	for rel in label.releases:
		releases.append(rel.title)
	return releases


# find all links in the html
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
		urls.append(video['file'].split('?v=')[1])
	return urls

# output the youtube links to actual html
# input is expected as a 2d array
def embedUrls(urls):
	f = open("output.html", "w")
	html_str = """
	<!doctype html>
	<html>
		<head> </head>
		<body>
	"""
	for url in urls:
		for link in url:
			html_str += "<iframe width=\"420\" height=\"315\" src=\"https://www.youtube.com/embed/" + link + "\"> </iframe>"
	html_str += """
		</body>
	</html>
	"""
	f.write(html_str)
	print("Succesfully wrote to output.html")
	f.close()

if __name__ == '__main__':
	i = int(sys.argv[1])
	releases = getReleaseIdsFromLabel(i)
	print(releases)
	urls = []
	for release in releases:
		try:
			urls.append(getURLFromRelease(release))
			print("Fetched urls from release nr. " + str(release))
		except AttributeError as e:
			print("Release nr. " + str(release) + " failed")
	print(urls)
	embedUrls(urls)


