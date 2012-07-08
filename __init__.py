import requests
from requests.auth import HTTPProxyAuth

from lxml import etree

import urlparse
import random
import time
import collections

EXCLUDED_LINK_EXTENSIONS = ('jpg', 'gif', 'jpeg','pdf', 'doc', 'docx', 'ppt', 'txt', 'png', 'zip', 'rar', 'mp3')

class Response(requests.Response):
	def xpath(self, xpath):
		if not hasattr(self, '_xpath'):
			self._xpath = etree.HTML(self.content)
		return [urlparse.urljoin(self.url, result) if isinstance(result, basestring) and result.split('@')[-1] in ('href', 'src', 'action') and not result.startswith('http') else result for result in self._xpath.xpath(xpath)]

	@property
	def domain(self):
		if not hasattr(self, '_domain'):
			self._domain = urlparse.urlparse(self.url).netloc
		return self._domain	

	def links(self):
		return [link.split('#')[0] for link in self.xpath('//a/@href')]

	def filter_links(self, links):
		return [link for link in links if not link.split('.')[-1].lower() in EXCLUDED_LINK_EXTENSIONS]

	def internal_links(self):
		return [link for link in self.links() if urlparse.urlparse(link).netloc == self.domain]

	def external_links(self):
		return [link for link in self.links() if link.startswith('http') and urlparse.urlparse(link).netloc != self.domain]

	def dofollow_links(self):
		return self.xpath('//a[@rel!="nofollow" or not(@rel)]/@href')
	
	def nofollow_links(self):
		return self.xpath('//a[@rel="nofollow"]/@href')

	def save(self, handle):
		if isinstance(handle, basestring):
			handle = open(handle, 'w')
		handle.write(self.content)
		handle.close()

	def title(self):
		title = self.xpath('//title/text()')
		if len(title):
			return title[0].strip()
		else:
			return None

class ProxyManager(object):
	def __init__(self, proxy, min_delay=10, max_delay=10):
		if isinstance(proxy, basestring):
			if proxy.startswith('http'):
				proxy = requests.get(proxy).content
			self.records = [line.strip() for line in proxy.strip().split('\n')]
		elif isinstance(proxy, collections.Iterable):
			self.records = proxy
		records = []
		for record in self.records:
			if '@' not in record:
				ip, port, username, password = record.split(':')
				record = username+':'+password+'@'+ip+':'+port
			records.append('http://'+record+'/')
		self.records = dict(zip(records, [0] * len(self.records)))

		self.min_delay = min_delay
		self.max_delay = max_delay

	@property
	def proxy(self):
		while True:
			records = [record for record, record_time in self.records.items() if record_time + random.randint(self.min_delay, self.max_delay) < time.time()]
			if len(records):
				record = random.sample(self.records, 1)[0]
				self.records[record] = time.time()
				return {'http': record, 'https': record}
			else:
				time.sleep(0.2)
		
requests.models.Response = Response