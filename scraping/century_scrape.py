########################################################################
# Scraper for century spring corp., to deal with ideosyncracies
# Provide entry point (generally, type of spring) and name/values to
# modify in POST request.  Will scrape data by decreasing range of asked
# value until there are <100 results, then increase range and repeat.
# All data scraped from tables is put in a CSV in folder 
# scrapes/CSC/<type>, with CSV titled by range they are generated from
#
# Future munging will be needed for price, etc.
########################################################################

import mechanize, time, math, codecs, sys
import lxml.html
#import re

minInput = float(sys.argv[1])
maxInput = float(sys.argv[2])

def extract_springs(page, springFile):
	html = lxml.html.fromstring(page)
	if len(html.find_class('tablesorter'))<1:
		return 0
	else:
		springTable = html.find_class('tablesorter')[0]
		springs = springTable.cssselect('tbody')[0].cssselect('tr')
		for spring in springs:
			line = []
			for cell in spring.getchildren():
				line.append(cell.text_content())
			toWrite = '|'.join(line)
			toWrite = 'newline'.join(toWrite.split('\n'))
			toWrite = toWrite + '|\n'
			springFile.write(toWrite)
		return len(springs)

def log(message):
	"""replace print with log to save&display print commands"""
	logFile = open('CSC-extension-'+sys.argv[1]+'.log','a')
	logFile.write(time.ctime()+': '+message+'\n')
	logFile.close()
	print(message)

url = 'http://www.centuryspring.com/Store/'
endpoint = 'search_extension.php'

#csv = codecs.open('CSC-extension.csv', encoding='utf-8', mode='w')
header = '|'.join(['select','Select','CAD','CSC','Stock #','OD (in)','ID (in)',
	'Free Length(in)','Rate (lbs/in)','Sugg. Max Defl (in)',
		'Sugg. Max Load (lbs)','Solid Length (in)','Wire Dia. (in)',
		'Total Coils','Material','Ends','Finish','\n'])
#csv.write(header)
#csv.close()
csv = codecs.open('CSC-extension-'+sys.argv[1]+'.csv', encoding='utf-8', mode='a')

#maxInput = 1000
#minInput = 0
scraping = True

br = mechanize.Browser() #from https://views.scraperwiki.com/run/python_mechanize_cheat_sheet/?
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
#br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open(url+endpoint)

loopMin = minInput
loopMax = maxInput

flag = "Your search has returned at least 100 rows, please filter your specifications further"

totalSprings = 2402

while scraping:
	searching = True
	while searching:
		br.select_form(name='CompForm')
		#print(br.form)
		br['filter6rg'] = ['1']
		br['filter6min'] = str(loopMin)
		br['filter6max'] = str(loopMax)
		#print(br.form)
		response = br.submit(name = 'WADbSearch1')#from: http://stackoverflow.com/questions/734893/python-mechanize-two-buttons-of-type-submit
		page = response.read()
		
		if flag not in page:	
			log('search successful, bounds ' +str(loopMin)+', '+str(loopMax))
			numSprings = extract_springs(page, csv)
			totalSprings += numSprings
			log('extracted '+str(numSprings)+' springs, '+str(totalSprings)+' total')
			searching = False
			diff = loopMax-loopMin
			loopMin = loopMax+0.01
			loopMax = (10*diff) + loopMin #maxInput
			if loopMin >= maxInput:
				log('scrape complete')
				scraping = False
		elif (loopMin > 10) and (0.0 < loopMax-loopMin < 0.2):
			log('Cannot slice, taking top 100 at ' +str(loopMin)+', '+str(loopMax))
			numSprings = extract_springs(page, csv)
			totalSprings += numSprings
			log('extracted '+str(numSprings)+' springs, '+str(totalSprings)+' total')
			searching = False
			diff = loopMax-loopMin
			loopMin = loopMax+0.01
			loopMax = (10*diff) + loopMin #maxInput
			if loopMin >= maxInput:
				log('scrape complete')
				scraping = False
		else:
			log('Bounds too large: '+str(loopMin)+', '+str(loopMax))
			loopMax = math.floor(100*(loopMax - ((loopMax-loopMin)/2.0)))/100.0
			if loopMax-loopMin < 0.001:
				log('unable to slice results, aborting')
				log(str(loopMax)+', '+str(loopMin))
				searching = False
				scraping = False
		time.sleep(0.5)
		br.back()
