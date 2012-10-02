import urllib2
import os
from bs4 import BeautifulSoup
from collections import deque
from urlparse import urlparse,urljoin
from shutil import copy2

counter = 0
local = []
visited = []
link = deque()
link.append('http://docs.python.org/tutorial/datastructures.html')
link.append('http://docs.python.org/library/urlparse.html')
link.append('http://docs.python.org/release/3.0.1/whatsnew/3.0.html')
link.append('http://docs.python.org/py3k/whatsnew/3.2.html')

def get_file(url):
	file_name = url.split('/')[-1]
	if url.find('.html') + 1:
		return
	remote_file = urllib2.urlopen(url)
	o = urlparse(url)
	temp = o.path
	temp = '/home/karthik/Projects/crawl' + temp
	ind = temp.find(file_name)
	temp1 = temp[:ind]
	if not os.path.exists(temp1):
		os.makedirs(temp1)
	ext = open(temp, 'w')
	ext.write(remote_file.read())
	ext.close()
	local.append(temp)
	visited.append(url)

for i in link:
	response = urllib2.urlopen(i)
	html_doc = response.read()
	soup = BeautifulSoup(html_doc)
	ext_files = soup.find_all('link', rel='stylesheet') + soup.find_all('script')
	for j in ext_files:
		try:
			temp = j['src']
		except KeyError:
			try:
				temp = j['href']
			except KeyError:
				continue
		temp1 = urljoin(i,temp)
		if temp1 in visited:
			continue
		get_file(temp1)
		counter = counter + 1
print counter
