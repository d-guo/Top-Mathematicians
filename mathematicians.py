from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

"""
create list of mathematicians' names
	retrieve html file
	parse through html file
	prevent duplicates of names using set
	return list

find popularity score of each mathematician
	record those who do not exist
"""

def get_content(url) : #retrieves html file of given url
	try :
		resp = get(url)
	except :
		log_error("request error")
		return None
	
	if file_is_valid(resp) :
		return resp.content
	else :
		log_error("url format not supported")
		return None

def file_is_valid(resp) :	#checks file to make sure it is html type
	content_type = resp.headers['Content-Type'].lower()
	if content_type.find('html') > -1 :
		return True
	return False

def log_error(error) : #logs error wip
	#print(error)

def list_of_names(raw_content) :	#returns list of name of mathematicians without duplicates
	names = set()
	html = BeautifulSoup(raw_content, 'html.parser')
	for li in html.select('li') :
		namelist = li.text.split("\n")
		for name in namelist :
			if len(name) > 0 :
				names.add(name)
	names = list(names)
	return names

def get_pop_num(name) : #returns the popularity score of a given mathematician (returns -1 if mathematician does not exist or can not be found)
	url = "https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/{}"
	raw_html = get_content(url.format(name))
	if raw_html == None :
		return -1
	html = BeautifulSoup(raw_html, 'html.parser')
	for a in html.select('a') :	#popularity score determined by number of searches in last six months
		if a['href'].find('latest-60') > -1 :
			a = a.text.replace(',', '')
			try :
				return int(a)
			except :
				return -1
	return -1

names = list_of_names(get_content("http://www.fabpedigree.com/james/mathmen.htm"))

final_result = []
for name in names :
	final_result.append((get_pop_num(name), name))

final_result.sort()
final_result.reverse()

print("Top Mathematicians (in last six months): ")
for i in range(0, len(final_result)) :
	print("{} with {} hits".format(final_result[i][1], final_result[i][0]))

unfound = 0
for i in range(0, len(final_result)) :
	if final_result[i][0] == -1 :
		unfound += 1
print("{} mathematicians not found".format(unfound))