import collections, itertools, simplejson, math

def cost(K, price):
	Kt = 1.0
	if abs((K-Kt))<0.1:
		return price
	else:
		return 1000000

Spring = collections.namedtuple('Spring', ['CSCname', 'OD', 'freeLength', 'K', 'preload', 'maxDef', 'maxLoad', 'wireDia', 'material', 'finish', 'price', 'weight'])

springDB = open('CSC-extension-all.csv', 'r')

row = 0
springs = []

for line in springDB:
	row += 1
	data = line.split('|')
	try:
		data = [data[0]]+[float(x) for x in data[1:8]]+[data[8]]+[data[9]]+[float(data[10])]
		data[1] *= 0.0254 #unit conversion, all in m or N
		data[2] *= 0.0254
		data[3] *= 4.53/0.0254
		data[4] *= 0.453
		data[5] *= 0.0254
		data[6] *= 0.453
		data[7] *= 0.0254
		weight = (0.3)*((2*data[7])*math.pi*2*data[2])*7800#mass in kg
		data.append(weight)
		tempSpring = Spring._make(data)
		springs.append(tempSpring)
	except  ValueError:
		pass
		#print 'Could not properly convert data for row '+str(row)

oneSpringCost = lambda spring: cost(spring.K, spring.price)

#bestSingle = min(springs, key = oneSpringCost)

twoSpringSeriesCost = lambda springPair: cost(((springPair[0].K*springPair[1].K)/(springPair[0].K+springPair[1].K)), (springPair[0].price+springPair[1].price))
twoSpringParallelCost = lambda springPair: cost((springPair[0].K+springPair[1].K), (springPair[0].price+springPair[1].price))

#bestSeries = min(itertools.combinations(springs, 2), key = twoSpringSeriesCost)
#bestParallel = min(itertools.combinations(springs, 2), key = twoSpringParallelCost)

jsonDump = simplejson.dumps(springs, separators=(',', ':'), sort_keys=True, indent=4 * ' ')
jsonDump = '\n'.join([l.rstrip() for l in  jsonDump.splitlines()])
jsonFile = open('CSC-extension.json', 'w')
jsonFile.write(jsonDump)
jsonFile.close()
