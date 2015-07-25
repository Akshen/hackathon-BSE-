# LinkedIn scrapper
# Author: Ashish Gaikwad <ash.gkwd@gmail.com>

import sys
import StringIO
import pycurl
import pymongo
from bs4 import BeautifulSoup
# TODO: store in mongoDB. Collections: raw linkedIn and filtered linkedIn

def mongo_dump(url, data, databse_name='hackathondb'):
	connection = pymongo.Connection('localhost', 27017)
	db = connection[databse_name]
	collection = db.linkedIn_raw_data
	# print collection.find({'url':url})
	collection.insert({
		'url' : url,
		'data': data
		})

def mongo_dump_filtered(url, data, databse_name='hackathondb'):
	connection = pymongo.Connection('localhost', 27017)
	db = connection[databse_name]
	collection = db.linkedIn_filtered_data
	# print collection.find({'url':url})
	collection.insert({
		'url' : url,
		'data': data
		})

def get_page(url):
	USER_AGENT_IPHONE = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
	# TODO: Download from url using curl
	f = StringIO.StringIO()
	curl = pycurl.Curl()
	curl.setopt(pycurl.USERAGENT, USER_AGENT_IPHONE)
	curl.setopt(pycurl.URL, url)
	curl.setopt(pycurl.WRITEFUNCTION, f.write)
	curl.perform()
	mongo_dump(url, f.getvalue())
	return f.getvalue()


def extract(html):
	EXPERIENCE_ID = '#background-experience'
	EDUCATION_ID = '#background-education'
	DIV_TAG = 'div'
	HEADER_TAG = 'header'
	EXPERIENCE_DATE_CLASS = 'experience-date-locale'
	LOCALITY_CLASS = '.locality'
	SUMMARY_TAG = 'h4'
	DEGREE_CLASS = 'degree'
	MAJOR_CLASS = 'major'
	EDUCATION_DATE_CLASS = 'education-date'
	experience = []
	education = []
	soup = BeautifulSoup(html)
	for work in soup.select(EXPERIENCE_ID + ' > ' + DIV_TAG):
		if work is not None:
			header = work.find(HEADER_TAG)
			subheader = work.find(class_=EXPERIENCE_DATE_CLASS)
			if header is not None:
				header = header.get_text()
			if subheader is not None:
				subheader = subheader.get_text()
			experience.append({
				"header": header,
				"subheader": subheader
				})
	for college in soup.select(EDUCATION_ID + ' > ' + DIV_TAG):
		if college is not None:
			summary = college.find(SUMMARY_TAG)
			degree = college.find(class_=DEGREE_CLASS)
			major = college.find(class_=MAJOR_CLASS)
			date = college.find(class_=EDUCATION_DATE_CLASS)
			education.append({
				"summary": summary.get_text() if summary is not None else None,
				"degree": degree.get_text() if degree is not None else None,
				"major": major.get_text() if major is not None else None,
				"date": date.get_text() if date is not None else None
				})
	return (experience, education)

def main():
	url = sys.argv[1]
	mongo_dump_filtered(url, extract(get_page(url)))

if __name__ == '__main__':
	main()