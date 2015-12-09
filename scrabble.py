import argparse
from requests_futures.sessions import FuturesSession
import re
import urlparse
import argparse

session = FuturesSession(max_workers=10)
image_re = re.compile(r'src="(.*?)"')
url = "http://www.google.com"
reqs = []
error_urls = []
result = []



def print_details(string):
	if showDetails:
		print string

def req_res(rs,base_url):
	#print "Base url :" + base_url
	res  = rs.result()
	#print res
	link_re = re.compile(r'href="(.*?)"')

	if(res.status_code != 200):
	    exit(0);
	#print res.status_code

	urls = []

	links = link_re.findall(res.text)
	images = image_re.findall(res.text)
	#print links

	for img in images:
		result.append(img)
		
	return urls


def crawl(urls,level):
	global reqs
	global result
	print_details("Level #" + str(level-1))
	print_details("Total # of links :" + str(len(result)))
	#print urls
	if level <= maxlevel and urls is not None and len(urls) > 0:
		returned_urls = []
		for eachurl in urls:
			returned_urls.append(reqs.append({"url":eachurl,"req":session.get(eachurl)}))
		
		for returned_urls in reqs:
			try:
				new_urls = req_res(returned_urls["req"],returned_urls["url"])
			except:
				error_urls.append(returned_urls["url"])
		crawl(new_urls,level+1)

parser = argparse.ArgumentParser()
parser.add_argument("--level", help="an integer to specify the level (default:2)", type=int)
parser.add_argument("--verbose", help="an integer to specify the level (default:2)", type=bool)
parser.add_argument('--url', help='link of the url to crawl', type=str,required=True)

args = parser.parse_args()



if args.url:
	url = args.url

if args.level:
	maxlevel = args.level
else:
	maxlevel = 1

if args.verbose:
	showDetails = True
else:
	showDetails = False

level = 1


res = session.get(url)
urls = req_res(res,url)
crawl(urls,level+1)




final_links = []
for link in result:
	if link not in final_links:
		final_links.append(link)
		if showDetails == False:
			print link

print_details("Total # of links : " +str(len(result)))
print_details("Total # of unique links : "+str(len(final_links)))
exit(0)
