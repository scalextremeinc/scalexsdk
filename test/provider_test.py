import scalex

providers = []

def setup():
	global providers
	providers = scalex.provider.getProviders()

# def test_getProviders():
# 	providers = scalex.provider.getProviders()

def test_getEstimatedCost():
	scalex.provider.getEstimatedCost(providers[0])

def test_getActualCost():
	scalex.provider.getActualCost(providers[0])

def test_getServers():
	scalex.provider.getServers(providers[0])

def test_performAction():
	servers = scalex.provider.getServers(providers[0])
	print servers[0]
	scalex.provider.performAction(providers[0], servers[0], 'poweron')
