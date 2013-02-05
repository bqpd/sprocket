import urllib2, re, time

def log(message):
	"""replace print with log to save&display print commands"""
	logFile = open('CSC-pricing.log','a')
	logFile.write(time.ctime()+': '+message+'\n')
	logFile.close()
	print(message)

priceRegex = re.compile("List Price: \$[0-9]+[\.[0-9]*]?")

springs = open('CSC-extension-1000.csv', 'r')
springs.next()
springList = open('CSC-extension-all.csv', 'a')

length = 121
start = time.clock()

scraped = 0
for line in springs:
	data = line.split('|')
	partNum = data[2]
	#print(partNum)
	resp = urllib2.urlopen('http://www.centuryspring.com/Store/item_detail.php?StockNumber='+partNum)
	page = resp.read()
	prices = priceRegex.findall(page)
	if len(prices)>0:
		price = prices[0]
		price = price.split('$')[1]
	else:
		price = 'UNAVAILABLE'
	resp.close()
	#print price
	data = data[2:12]
	data.append(price)
	data.append('\n')
	toWrite = '|'.join(data)
	log(toWrite)
	springList.write(toWrite)
	scraped += 1
	estimate = ((time.clock()-start)/float(scraped))*(length-scraped)
	log('Scraped '+str(scraped)+' of '+str(length)+' in '+str(time.clock()-start)+' seconds, ETC: '+str(estimate))
	time.sleep(0.05)
