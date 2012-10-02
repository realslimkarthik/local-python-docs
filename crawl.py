import urllib2
from bs4 import BeautifulSoup
from collections import deque
from urlparse import urlparse,urljoin

link = deque()
link.append('http://docs.python.org/tutorial/datastructures.html')
visited = []


def link_collect(url):
	if url in visited:
		link.remove(url)
		return -1
	visited.append(url)
	response = urllib2.urlopen(url)
	html_doc = response.read()
	soup = BeautifulSoup(html_doc)
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
			ext_files = soup.find_all('link', rel='stylesheet') + soup.find_all('script')
			



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

print visited
