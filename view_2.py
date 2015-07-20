import urllib,urllib2
import requests
import urlparse
import pycurl
import xlrd
import json
import StringIO
from bs4 import BeautifulSoup



filename = xlrd.open_workbook('hackathon_social_media_v1.xlsx',on_demand=True)
searchlist = open('Searchlist.txt','w+')



def info_take(filename,cols=None):
	for s in filename.sheets():
		for row in range(1,s.nrows):
			for col in range(len(cols)):
				searchlist.write(s.cell(row,cols[col]).value) #Add more niche for better performance.
			searchlist.write('\n')	

	return searchlist


def getPage(user_url):
	f = StringIO.StringIO()
	user_url = map(str,user_url.split(" "))

	user_url = "+".join(user_url)
	user_url = user_url[:-1]
	search_url = 'https://www.google.co.in/search?&q=%s' % user_url
	curl = pycurl.Curl()
	curl.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (iPhone; U; CPpyUurl iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5')
	curl.setopt(pycurl.URL, search_url)
	curl.setopt(pycurl.WRITEFUNCTION,f.write)

	curl.perform()
	return f.getvalue()
	


def google_search(searchlist):
	result = open('search_results.txt','w')
	searchlist = open('Searchlist.txt','r')
	listline = searchlist.readlines()
	for s in xrange(len(listline)):
		data = getPage(listline[s])
		
		soup = BeautifulSoup(data, "html.parser")
		# for link in soup.find_all(class_=["f","kv","_SWb"]):
		for link in soup.select('a[href*="linkedin.com"]'):
			parsed = urlparse.urlparse(link["href"])
			try:
				link = str(urlparse.parse_qs(parsed.query)['q'][0])
				result.write(link + '\n')
			except:
				continue
		 	

		

	result.close()
	searchlist.close()

if __name__ == '__main__':
	result = info_take(filename,cols=[0])
	google_search(result)
   
