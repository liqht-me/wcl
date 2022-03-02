import requests
from bs4 import BeautifulSoup


class Website:
	def __init__(self, url: str):
		self.url = url
		self.rawPage = requests.get(url)
		self.contentSoup = BeautifulSoup(self.rawPage.content, 'html.parser')
		self.foundURLs = self.contentSoup.find_all('a', href=True)

	def getValidURLs(self):
		for urlObject in self.foundURLs:
			hitURL = urlObject['href']
			if hitURL == '#':
				continue
			elif hitURL.startswith('/'):
				yield self.url + hitURL
			else:
				yield hitURL


class Crawler:
	def __init__(self, startURL):
		self.urlPool = []
		self.deniedURLs = []
		self.crawledURLs = []
		self.websites = []
		self.getDeniedURLs(startURL)
		self.crawl(startURL)
		self.mainLoop()

	def getDeniedURLs(self, rootURL):
		deniedPages = requests.get(f"{rootURL}/robots.txt").text
		if 'User-agent: *' in deniedPages:
			for line in deniedPages.split('\n'):
				if (data := line.split(' '))[0] == 'Disallow:':
					print(f"Denied @ {f'{rootURL}{data[1]}' if data[1].startswith('/') else data[1]}")
					self.deniedURLs.append(f'{rootURL}{data[1]}' if data[1].startswith('/') else data[1])

	def crawl(self, url):
		print(f'{url};'
		      f'{len(self.urlPool)};'
		      f'{len(self.crawledURLs)}')

		website = Website(url)
		self.crawledURLs.append(url)
		self.websites.append(website)

		for crawledURL in website.getValidURLs():
			if (crawledURL not in self.crawledURLs) \
					and (crawledURL not in self.deniedURLs) \
					and crawledURL not in self.urlPool:
				self.urlPool.append(crawledURL)

	def mainLoop(self):
		for url in self.urlPool:
			self.crawl(url)
		print(self.crawledURLs)


if __name__ == '__main__':
	Crawler('https://www.philips.de')
