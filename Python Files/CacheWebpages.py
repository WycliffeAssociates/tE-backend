import urllib2

# which URL should we cache?
url = 'http://td.unfoldingword.org/exports/langnames.json'

# opens the URL and read the page
response = urllib2.urlopen(url)
webContent = response.read()

# create a new JSON file called 'languages'
jsonFile = open("languages.json", "w")
# write all the web content that was read from it to the file
jsonFile.write(webContent)
#close the file writer
jsonFile.close()