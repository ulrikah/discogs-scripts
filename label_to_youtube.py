#!/usr/bin/env python3

import sys
import discogs_client

d = discogs_client.Client('YoutubeURLFromLabel/0.1')

# returns Release objects
def getReleasesFromLabel(label):
	return d.label(label).releases

# returns a list of urls from a Release object
def getYoutubeURLsFromRelease(release):
	return [videos.url.split("v=")[1] for videos in release.videos]


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
	label_id = int(sys.argv[1])
	releases = getReleasesFromLabel(label_id)
	urls = []
	for release in releases:
		try:
			urls.append(getYoutubeURLsFromRelease(release))
			print("Fetched urls from release nr. " + str(release))
		except:
			print("Release nr. " + str(release) + " failed")
	print(urls)
	embedUrls(urls)


