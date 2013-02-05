import csv, simplejson, collections
motorFile = open('motors.csv', 'r')

motors = []
Motor = collections.namedtuple('Motor', ['part', 'name', 'shaftDia', 'power', 'voltage', 'speed', 'torque', 'price','weight'])
#mm, W, V, rpm, mNm respectivly

lineReader = csv.reader(motorFile, delimiter = ',', quotechar = '"')
e=0
for line in lineReader:
	try:
		data = line[:2]+[float(x.split(' ')[0]) for x in line[2:7]]+[float(line[7].split(' ')[1])]
		data[2] /= 1000.0 #converting to m/N
		data[5] *= (3.1415*2)/60.0 #rad/sec
		data[6] /= 1000.0
		weight = data[3]/data[5]*1000#fake
		data.append(weight)
		tempMotor = Motor._make(data)
		motors.append(tempMotor)
	except:
		e+=1
		print "Value error"

jsonDump = simplejson.dumps(motors, separators=(',', ':'), sort_keys=True, indent=4 * ' ')
jsonDump = '\n'.join([l.rstrip() for l in  jsonDump.splitlines()])
jsonFile = open('motors.json', 'w')
jsonFile.write(jsonDump)
jsonFile.close()
