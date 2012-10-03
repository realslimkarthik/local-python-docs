import urllib2
import os
from bs4 import BeautifulSoup
from collections import deque
from urlparse import urlparse,urljoin

location = '/var/www/pydocs/'
link = deque()
link.append('http://docs.python.org/tutorial/datastructures.html')
visited = []

def get_file(url, remote_file):
	file_name = url.split('/')[-1]
	o = urlparse(url)
	temp = o.path
	temp = location + temp
	ind = temp.find(file_name)
	temp1 = temp[:ind]
	if not os.path.exists(temp1):
		os.makedirs(temp1)
	ext = open(temp, 'w')
	ext.write(remote_file)
	ext.close()


def link_collect(url):
	if url in visited:
		link.remove(url)
		return -1
	visited.append(url)
	response = urllib2.urlopen(url)
	html_doc = response.read()
	get_file(url,html_doc)
	if url.find('.html') + 1:
		soup = BeautifulSoup(html_doc)
	else:
		return
	for hRef in soup.find_all('a'):
		try:
			hRef['href']
		except KeyError:
			continue
		else:
			if hRef['href'].find('#') + 1:
				continue
			elif hRef['href'].find('.html') + 1:
				temp = hRef.get('href')
				o = urlparse(urljoin(url,temp))
				if o.netloc == 'docs.python.org':
					if o.geturl() not in visited:
						link.append(o.geturl())
			ext_files = soup.find_all('link') + soup.find_all('script')
			for j in ext_files:
				try:
					temp = j['src']
				except KeyError:
					try:
						temp = j['href']
					except KeyError:
						continue
				temp1 = urljoin(url,temp)
				if temp1 in visited:
					continue
				else:
					link.append(temp1)



while (link):
	print link[0]
	i = link_collect(link[0])
	try:
		link.popleft()
	except IndexError:
		break
	else:
		if i!=-1:
			print len(visited)
