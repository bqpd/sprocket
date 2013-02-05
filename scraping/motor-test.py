<head></head>
<body>
<script type="text/javascript">
//<![CDATA[

window.deflection = 2*3.1415*(15/360.0);
window.rMax = 1;
window.torqueMax = 10;
window.torqueSense = 0.1;


window.Cost = function(part) {
	return part['price'];
}

function Filter(encoder) {
	var ppr = (window.torqueMax/window.torqueSense)/(window.deflection);
	if (ppr <= encoder['resolution']) { return true; }
	else { return false }
}


