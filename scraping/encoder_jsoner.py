import csv, simplejson, collections
encoderFile = open('encoders.csv', 'r')

encoders = []
Encoder = collections.namedtuple('Encoder', ['part', 'price', 'type', 'resolution', 'weight'])
#0, 5, 6, 8(c/ppr) respectivly

lineReader = csv.reader(encoderFile, delimiter = ',', quotechar = '"')
e=0
for line in lineReader:
	try:
		data = [line[0]]+[float(line[5])]+[line[6]]+[float(line[8])]+[0.005]
		tempEnc = Encoder._make(data)
		encoders.append(tempEnc)
	except:
		e+=1
		print "Value error"

jsonDump = simplejson.dumps(encoders, separators=(',', ':'), sort_keys=True, indent=4 * ' ')
jsonDump = '\n'.join([l.rstrip() for l in  jsonDump.splitlines()])
jsonFile = open('encoders.json', 'w')
jsonFile.write(jsonDump)
jsonFile.close()

