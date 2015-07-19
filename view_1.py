import xlrd
import json
import urllib,google
import time

filename = xlrd.open_workbook('hackathon_social_media_v1.xlsx',on_demand=True)
searchlist = open('Searchlist.txt','w')



def info_take(filename,cols=None):
	for s in filename.sheets():
		for row in range(1,s.nrows):
			for col in range(len(cols)):
				searchlist.write(s.cell(row,cols[col]).value + '\t')
			searchlist.write('\n')	

	return searchlist
	# searchlist.close()

def get_data_object(s):
	query = urllib.urlencode({'q': s})
  	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % query
  	search_response = urllib.urlopen(url)
  	search_results = search_response.read()

  	results = json.loads(search_results)
  	data = results['responseData']
  	return data



def google_search(searchlist):
	result = open('search_results.txt','w')
	searchlist = open('Searchlist.txt','r')
	listline = searchlist.readlines()

	for s in xrange(len(listline)):
		data = get_data_object(listline[s])
	  	if type(data) is type(None):
	  		time.sleep(100)
	  		data = get_data_object(listline[s])
  		hits = data['results']
  		for h in hits:
  			if 'linkedin' in h['url']:
  				result.write(h['url'] + '\n')
  				break
	  	
	  	

	result.close()
	searchlist.close()


if __name__ == '__main__':
	result = info_take(filename,cols=[0,11])
	google_search(result)


