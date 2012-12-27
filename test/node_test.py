import sys
import scalex

winNodes = []
linuxNodes = []
nodes = []

def setup():
  global winNodes
  global linuxNodes
  global nodes
  winNodes = scalex.node.getNodes(platform = 'Windows')
  linuxNodes = scalex.node.getNodes(platform = 'Linux')
  nodes.extend(linuxNodes)
  nodes.extend(winNodes)


# getNodes()
# def test_getNodes():
#

# getUpdates() and applyUpdates()
def test_getUpdates():
  if linuxNodes == []:
    sys.stderr.write('**ERROR: NO Linux nodes, skip getUpdates_test()\n')
    return
  updates = []
  node = {}
  for i in linuxNodes:
    updates = scalex.node.getUpdates(i)
    if updates != []:
      node = i
      break
  if updates == []:
    sys.stderr.write('**ERROR: NO updates, skip applyUpdates()\n')
    return
  scalex.node.applyUpdates('test_name', node, updates[0])

# getPatches() and applyPatches()
def test_getPatches():
  if winNodes == []:
    sys.stderr.write('**ERROR: NO Windows nodes, skip getPatches_test()\n')
    return
  scalex.node.getPatches(winNodes[0])
  patches = []
  node = {}
  for i in winNodes:
    patches = scalex.node.getPatches(i)
    if patches != []:
      node = i
      break
  if patches == []:
    sys.stderr.write('**ERROR: NO patches, skip applyPatches()\n')
    return
  scalex.node.applyPatches('test_name', node, patches[0])

# getAudits()
def getAudits_test():
  if linuxNodes == []:
    sys.stderr.write('**ERROR: NO Linux nodes, skip getAudits_test()\n')
    return
  scalex.node.getAudits(linuxNodes[0])

# getAllAgentsWithPatch()
def getAllAgentsWithPatch_test():
  if nodes == []:
    sys.stderr.write('**ERROR: NO nodes, skip getAllAgentsWithPatch_test()\n')
    return
  updates = []
  for i in nodes:
    updates = scalex.node.getUpdates(i)
    if updates != []:
      break
  if updates == []:
    sys.stderr.write('**ERROR: NO updates/patches, skip getAllAgentsWithPatch_test()\n')
  scalex.node.getAllAgentsWithPatch(updates[0])

# getGroups() and getNodesOfGroup()
def getGroups_test():
  groups = scalex.node.getGroups()
  if groups == []:
    sys.stderr.write('**ERROR: NO groups, skip getNodesOfGroup()\n')
    return
  scalex.node.getNodesOfGroup(groups[0])
  
    
  

  
