import scalex

nodes = []

def setup():
	global nodes
	nodes = scalex.node.getNodes()

def test_getRollupAlerts():
	scalex.monitor.getRollupAlerts()

def test_getStatus():
	scalex.monitor.getStatus(nodes[0])

def test_enable():
	scalex.monitor.enableMonitoring(nodes[0])
	scalex.monitor.disableMonitoring(nodes[0])

def test_getAlertsForNode():
	scalex.monitor.getAlertsForNode(nodes[0])

def test_enableAlerts():
	scalex.monitor.enableAlerts(nodes[0])

def test_disableAlerts():
	scalex.monitor.disableAlerts(nodes[0])

def test_getEvents():
	scalex.monitor.getEvents(nodes[0])

def test_getMetrics():
	scalex.monitor.getMetrics(nodes[0])