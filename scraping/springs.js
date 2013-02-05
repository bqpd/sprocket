window.deflection = 2*3.1415*(15/360.0);
window.rMax = 5;
window.torqueMax = 5;
window.error = 1;


window.Cost (part) {
	return part['price'];
}

Filter (spring) {
	float r = spring['maxDef']/window.deflection;
	if (r < window.rMax) {
		float Kt = window.torqueMax/window.deflection;
		Kt = Kt/(r**2);
		if (Math.abs(K-Kt)<window.error) {
			return true;
		}
		else {return false;}
	}
	else {return false;}
}

object tempSpring;
float bestCost;
object best;

for (i = springs.length; i>0; i--) {
	for (j = 0; j<=i; j++) {
		tempSpring = {'spring1':springs[i], 'spring2':springs[j], 
				'K':(springs[i]['K']*springs[j]['K'])/(springs[i]['K']+springs[j]['K']),
				'price':springs[i]['price']+springs[j]['price'],
				'weight':springs[i]['weight']+springs[j]['weight'],
				'maxDef':springs[i]['maxDef']+springs[j]['maxDef'],
				'type':'series'};
		if (Filter(tempSpring)) {
			if (window.Cost(tempSpring) < bestCost) {
				best = tempSpring;
				bestCost = window.Cost(tempSpring);
			}
		tempSpring['K'] = (springs[i]['K']+springs[j]['K'])
		maxDef = (springs[i]['maxDef']<springs[j]['maxDef']) ? (springs[i]['maxDef']) : (springs[j]['maxDef'])
		tempSpring['type'] = 'parallel'
		if (Filter(tempSpring)) {
			if (window.Cost(tempSpring) < bestCost) {
				best = tempSpring;
				bestCost = window.Cost(tempSpring);
			}
		}
	}
}
